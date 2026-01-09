import asyncio
import json
import logging
from http import HTTPStatus

from django import forms
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from postgrest.api_clients import ColumnMetadataApiClient
from postgrest.base.base_api_clients import ApiClient

# from postgrest.mocks.base.mock_base_api_clients import MockApiClient as ApiClient
# from postgrest.mocks.mock_api_clients import (
#     MockColumnMetadataApiClient as ColumnMetadataApiClient,
# )
from resource_management.forms import ResourceDeletionForm

from .forms.base_forms import (
    SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix,
    SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix,
)
from .services import get_categories_for_editor
from .utils import UNCATEGORISED_CATEGORY

logger = logging.getLogger(__name__)


class EditorCategoriesTemplateView(TemplateView):
    api_client: ApiClient
    column_metadata_api_client_class: type[ColumnMetadataApiClient]
    column_metadata_api_client: ColumnMetadataApiClient
    categories: dict
    category_names: list[str]
    column_metadata: list[dict]
    column_names: set[str]

    def setup(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        self.setup_column_metadata()
        self.setup_categories()
        return super().setup(request, *args, **kwargs)

    def setup_column_metadata(self):
        self.column_metadata = (
            self.column_metadata_api_client.get_resources_for_enabled_categories()
        )
        self.column_names = set(
            cm.get("column_name", "")
            for cm in self.column_metadata
            if cm.get("column_name", "")
        )

    def setup_categories(self):
        self.category_names = list(
            set(
                r.get("category", "") for r in self.column_metadata if r.get("category")
            )
        )
        self.category_names.sort()
        self.categories = get_categories_for_editor(
            self.api_client, self.column_metadata, self.category_names
        )

    def _get_first_category(self):
        return next(iter(self.category_names), None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "toc_list_items": self.categories,
                "category_names": self.category_names,
                "initial_category": self.category,
            }
        )
        return context


class EditorEnabledTabListTemplateView(EditorCategoriesTemplateView):
    template_name = "editor/toc_new/toc_base.html"


class EditorTocTemplateView(TemplateView):
    api_client: ApiClient
    column_metadata_api_client_class: type[ColumnMetadataApiClient]
    column_metadata_api_client: ColumnMetadataApiClient
    categories: dict
    category_names: list[str]
    column_metadata: list[dict]
    column_names: set[str]

    def setup(self, request, *args, **kwargs):
        self.setup_column_metadata()
        self.setup_categories()
        return super().setup(request, *args, **kwargs)

    def setup_column_metadata(self):
        self.column_metadata = (
            self.column_metadata_api_client.get_resources_for_enabled_categories()
        )
        self.column_names = set(
            cm.get("column_name", "")
            for cm in self.column_metadata
            if cm.get("column_name", "")
        )

    def setup_categories(self):
        self.category_names = list(
            set(r.get("category", "") for r in self.column_metadata)
        )
        self.category_names.sort()
        self.categories = get_categories_for_editor(
            self.api_client, self.column_metadata, self.category_names
        )

    def _get_first_category(self):
        return next(iter(self.category_names), None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "toc_list_items": self.categories,
            }
        )
        return context


class EditorStartFormView(
    EditorTocTemplateView,
    FormView,
):
    api_client: ApiClient
    pk_field_name: str
    editor_reverse_base: str
    resource_type_readable: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": f"New {self.resource_type_readable.title()}",
            }
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
            }
        )
        return kwargs

    def form_valid(self, form):
        new_resource = self.api_client.register(form.cleaned_data)
        messages.success(
            self.request,
            f"New {self.api_client.endpoint_definition.definition_name} registered.",
        )
        self.success_url = reverse_lazy(
            self.editor_reverse_base,
            kwargs={"resource_id": new_resource.get(self.pk_field_name)},
        )
        return super().form_valid(form)


class EditorForeignKeyFieldsTemplateView(TemplateView):
    resource: dict
    resource_id: int
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    editor_reverse_base: str

    new_one_to_one_relation_reverse_base: str
    update_one_to_one_relation_reverse_base: str
    delete_one_to_one_relation_reverse_base: str
    new_one_to_many_relation_reverse_base: str
    update_one_to_many_relation_reverse_base: str
    delete_one_to_many_relation_reverse_base: str

    async def get_one_to_one_field_metadata(self) -> dict:
        one_to_one_field_metadata = dict()
        one_to_one_fields = (
            self.api_client.endpoint_definition.get_user_specifiable_one_to_one_fields()
        )

        for field_name, field_metadata in one_to_one_fields.items():
            fk_table_name = field_metadata.get("fk_table_name", "")
            fk_api_client = ApiClient.get_client_instance_by_endpoint(fk_table_name)
            if not fk_api_client:
                continue
            new_form = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix(
                fk_api_client,
                ColumnMetadataApiClient(),
                id_prefix="new",
            )
            initial = dict()
            fk_resource_id = None
            try:
                fk_resource_id = self.resource.get(field_name)
            except AttributeError:
                pass
            if fk_resource_id:
                existing_resource = fk_api_client.get(fk_resource_id)
                initial = existing_resource
            one_to_one_field_metadata.update(
                {
                    field_name: {
                        "new_form": new_form,
                        "update_form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                            fk_api_client,
                            ColumnMetadataApiClient(),
                            id_suffix=f"{fk_table_name}_{self.resource_id}",
                            initial=initial,
                        ),
                        "delete_form": ResourceDeletionForm(
                            initial={"resource_id_to_delete": fk_resource_id}
                        ),
                        "type_readable": fk_api_client.type_readable,
                        "type_readable_plural": fk_api_client.type_readable_plural,
                    },
                }
            )
        return one_to_one_field_metadata

    async def get_one_to_many_field_metadata(self) -> dict:
        one_to_many_field_metadata = dict()
        one_to_many_fields = self.api_client.endpoint_definition.get_user_specifiable_one_to_many_fields()
        for field_name, field_metadata in one_to_many_fields.items():
            fk_table_name = field_metadata.get("fk_table_name", "")
            fk_api_client = ApiClient.get_client_instance_by_endpoint(fk_table_name)
            if not fk_api_client:
                continue
            new_form = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix(
                fk_api_client,
                ColumnMetadataApiClient(),
                id_prefix="new",
            )
            existing_resources = fk_api_client.get_resources_referencing_resource_id(
                field_metadata.get("fk_table_column_name"), self.resource_id
            )
            one_to_many_field_metadata.update(
                {
                    field_name: {
                        "new_form": new_form,
                        "resource_forms": {
                            existing_resource.get(
                                fk_api_client.endpoint_definition.pk_field_name
                            ): {
                                "update_form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                                    fk_api_client,
                                    ColumnMetadataApiClient(),
                                    id_suffix=f"{fk_table_name}_{fk_api_client.endpoint_definition.pk_field_name}",
                                    initial=existing_resource,
                                ),
                                "delete_form": ResourceDeletionForm(
                                    initial={
                                        "resource_id_to_delete": existing_resource.get(
                                            fk_api_client.endpoint_definition.pk_field_name
                                        )
                                    }
                                ),
                            }
                            for existing_resource in existing_resources
                        },
                        "type_readable": fk_api_client.type_readable,
                        "type_readable_plural": fk_api_client.type_readable_plural,
                        "templates": {
                            "update_dialog": render_to_string(
                                "editor/dialogs/update_dialog.html",
                                {
                                    "form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                                        fk_api_client,
                                        ColumnMetadataApiClient(),
                                        id_suffix="__resource_id__",
                                    ),
                                    "resource_id": "__resource_id__",
                                    "update_resource_url": reverse_lazy(
                                        self.update_one_to_many_relation_reverse_base,
                                        kwargs={
                                            "resource_id": self.resource_id,
                                            "fk_column_name": field_name,
                                            "fk_resource_id": "__resource_id__",
                                        },
                                    ),
                                    "dialog_id": f"update-{field_name}-__resource_id__-dialog",
                                    "dialog_extra_classes": "col-lg-10",
                                    "resource_type_readable": fk_api_client.endpoint,
                                },
                            ),
                            "delete_dialog": render_to_string(
                                "editor/dialogs/delete_dialog.html",
                                {
                                    "form": ResourceDeletionForm(
                                        initial={
                                            "resource_id_to_delete": "__resource_id__"
                                        }
                                    ),
                                    "resource_id": "__resource_id__",
                                    "delete_resource_url": reverse_lazy(
                                        self.delete_one_to_many_relation_reverse_base,
                                        kwargs={
                                            "resource_id": self.resource_id,
                                            "fk_column_name": field_name,
                                            "fk_resource_id": "__resource_id__",
                                        },
                                    ),
                                    "dialog_id": f"delete-{field_name}-__resource_id__-dialog",
                                    "dialog_extra_classes": "col-lg-10",
                                    "resource_type_readable": fk_api_client.endpoint,
                                },
                            ),
                            "list_item": render_to_string(
                                "editor/foreign_key_fields/one_to_many_field_list_item.html",
                                {
                                    "form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                                        fk_api_client,
                                        ColumnMetadataApiClient(),
                                        id_suffix="__resource_id__",
                                    ),
                                    "resource_id": "__resource_id__",
                                    "resource_type_readable": fk_api_client.endpoint,
                                    "field": {"name": field_name},
                                },
                            ),
                        },
                    },
                }
            )
        return one_to_many_field_metadata


class EditorFormView(FormView):
    template_name = "editor/"
    form_class: forms.Form

    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    editor_overview_reverse_base: str
    resource_type_readable: str

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)

    def dispatch(self, request, *args, **kwargs):
        self.category = self.request.GET.get("category")
        self.success_url = reverse_lazy(
            self.editor_overview_reverse_base,
            kwargs={
                "resource_id": self.resource_id,
            },
        )
        self.title_base = f"{self.resource_type_readable.title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        update_data = form.cleaned_data
        try:
            self.api_client.update(self.resource_id, update_data)
        except Exception:
            error_msg = f"An error occurred whilst updating {self.resource_type_readable} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.form_invalid(form)

        message = "Successfully applied changes."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return redirect(self.success_url)
            # return super().form_valid(form)
        return JsonResponse(
            {
                "message": message,
                "redirect": self.success_url,
            }
        )

    def form_invalid(self, form):
        error_msg = "Some fields were invalid. Please see feedback below."
        if self.request.accepts("text/html"):
            messages.error(self.request, error_msg)
            return redirect(self.success_url)
            # return super().form_invalid(form)
        return JsonResponse(
            {
                "feedback": error_msg,
                "url": self.request.get_full_path(),
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "initial": self.resource,
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
            }
        )
        return kwargs


class EditorCategoryBasedFormView(EditorFormView):
    template_name = "editor/"
    form_class: forms.Form

    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    editor_overview_reverse_base: str
    resource_type_readable: str

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)

    def dispatch(self, request, *args, **kwargs):
        self.category = self.request.GET.get("category")
        if not self.category:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        self.success_url = reverse_lazy(
            self.editor_overview_reverse_base,
            kwargs={
                "resource_id": self.resource_id,
            },
        )
        self.title_base = f"{self.resource_type_readable.title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        update_data = form.cleaned_data
        try:
            self.api_client.update(self.resource_id, update_data)
        except Exception:
            error_msg = f"An error occurred whilst updating {self.resource_type_readable} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.api_invalid()

        message = f"Saved changes to {self.category}."
        return JsonResponse(
            {
                "message": message,
            }
        )

    def form_invalid(self, form):
        error_msg = "Some fields were invalid. Please see feedback below."
        return JsonResponse(
            {
                "message": error_msg,
                "feedback": json.loads(form.errors.as_json()),
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    def api_invalid(self):
        return JsonResponse(
            {
                "message": f"An error occurred whilst updating {self.resource_type_readable} {self.resource_id}. The update may not have been applied.",
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "initial": self.resource,
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
                "category": self.category,
            }
        )
        return kwargs


class EditorTabbedFormTemplateView(
    EditorFormView,
    EditorForeignKeyFieldsTemplateView,
    EditorCategoriesTemplateView,
    TemplateView,
):
    template_name = "editor/editor_tab.html"
    view_is_async = True

    editor_form_reverse: str
    editor_form_url: str

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        self.editor_form_url = reverse_lazy(
            self.editor_form_reverse, kwargs={"resource_id": self.resource_id}
        )
        return super().dispatch(request, *args, **kwargs)

    async def get(self, request, *args, **kwargs):
        field_metadata = await asyncio.gather(
            self.get_one_to_one_field_metadata(), self.get_one_to_many_field_metadata()
        )
        self.one_to_one_field_metadata = field_metadata[0]
        self.one_to_many_field_metadata = field_metadata[1]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "resource": self.resource,
                "resource_id": self.resource_id,
                "initial_category": self.category,
                "editor_form_url": self.editor_form_url,
                "one_to_one_field_metadata": self.one_to_one_field_metadata,
                "one_to_many_field_metadata": self.one_to_many_field_metadata,
                "new_one_to_one_relation_reverse_base": self.new_one_to_one_relation_reverse_base,
                "update_one_to_one_relation_reverse_base": self.update_one_to_one_relation_reverse_base,
                "delete_one_to_one_relation_reverse_base": self.delete_one_to_one_relation_reverse_base,
                "new_one_to_many_relation_reverse_base": self.new_one_to_many_relation_reverse_base,
                "update_one_to_many_relation_reverse_base": self.update_one_to_many_relation_reverse_base,
                "delete_one_to_many_relation_reverse_base": self.delete_one_to_many_relation_reverse_base,
            }
        )
        return context


class EditorProcessFormView(TemplateView):
    template_name = "editor/editor_base_new.html"

    api_client: ApiClient
    editor_overview_reverse_base: str
    toc_url: str
    tabbed_form_url: str
    tabbed_form_reverse: str
    resource_type_readable: str

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)
        self.category = request.GET.get("category", "")

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            self.editor_overview_reverse_base,
            kwargs={
                "resource_id": self.resource_id,
            },
        )
        self.tabbed_form_url = reverse_lazy(
            self.tabbed_form_reverse, kwargs={"resource_id": self.resource_id}
        )
        self.title_base = f"{self.resource_type_readable.title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title_base,
                "main_subheading": self.resource_type_readable.title(),
                "main_heading": self.title_base,
                "resource": self.resource,
                "resource_id": self.resource_id,
                "toc_url": self.toc_url,
                "tabbed_form_url": self.tabbed_form_url,
                "initial_category": self.category,
                "toast_template": render_to_string("editor/toast_template.html", {}),
            }
        )
        return context


class OneToOneRelationView(View):
    form_class = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.resource = self.api_client.get(self.resource_id)
        self.fk_column_name = self.kwargs["fk_column_name"]
        fk_fields = self.api_client.endpoint_definition.get_user_specifiable_foreign_key_fields()
        self.fk_table_name = fk_fields.get(self.fk_column_name, {}).get("fk_table_name")
        self.fk_api_client = ApiClient.get_client_instance_by_endpoint(
            self.fk_table_name
        )
        return super().dispatch(request, *args, **kwargs)


class OneToOneRelationBasedFormView(OneToOneRelationView, FormView):
    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": ApiClient.get_client_instance_by_endpoint(
                    self.fk_table_name
                ),
                "column_metadata_api_client": ColumnMetadataApiClient(),
                "id_prefix": "new",
            }
        )
        return kwargs


class NewOneToOneRelationFormView(OneToOneRelationBasedFormView):
    def form_valid(self, form):
        new_resource = self.fk_api_client.register(form.cleaned_data)
        new_resource.update(
            {
                "pk": new_resource.get(
                    self.fk_api_client.endpoint_definition.pk_field_name
                )
            }
        )
        self.api_client.update(
            self.resource_id,
            {
                self.fk_column_name: new_resource.get(
                    self.fk_api_client.endpoint_definition.pk_field_name
                )
            },
        )
        message = f"Added new {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": new_resource})


class UpdateOneToOneRelationFormView(OneToOneRelationBasedFormView):
    def form_valid(self, form):
        fk_resource_id = int(self.resource.get(self.fk_column_name))
        self.fk_api_client.update(fk_resource_id, form.cleaned_data)
        message = f"Updated {self.fk_table_name} registration."
        resource = self.fk_api_client.get(fk_resource_id)
        resource.update(
            {"pk": resource.get(self.fk_api_client.endpoint_definition.pk_field_name)}
        )
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource})


class DeleteOneToOneRelationFormView(OneToOneRelationView, FormView):
    form_class = ResourceDeletionForm

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def form_valid(self, form):
        fk_resource_id = int(self.resource.get(self.fk_column_name))
        self.fk_api_client.delete(fk_resource_id)
        self.api_client.update(self.resource_id, {self.fk_column_name: None})
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"result": "success"})


class OneToManyRelationView(View):
    form_class = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.resource = self.api_client.get(self.resource_id)
        self.fk_column_name = self.kwargs["fk_column_name"]
        one_to_many_fields = (
            self.api_client.endpoint_definition._get_one_to_many_fields()
        )
        self.fk_table_name = one_to_many_fields.get(self.fk_column_name, {}).get(
            "fk_table_name"
        )
        self.fk_table_column_name = one_to_many_fields.get(self.fk_column_name, {}).get(
            "fk_table_column_name"
        )
        self.fk_api_client = ApiClient.get_client_instance_by_endpoint(
            self.fk_table_name
        )
        return super().dispatch(request, *args, **kwargs)


class OneToManyRelationBasedFormView(OneToManyRelationView, FormView):
    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": ApiClient.get_client_instance_by_endpoint(
                    self.fk_table_name
                ),
                "column_metadata_api_client": ColumnMetadataApiClient(),
                "id_prefix": "new",
            }
        )
        return kwargs


class NewOneToManyRelationFormView(OneToManyRelationBasedFormView):
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        cleaned_data.update({self.fk_table_column_name: self.resource_id})
        new_resource = self.fk_api_client.register(cleaned_data)
        new_resource.update(
            {
                "pk": new_resource.get(
                    self.fk_api_client.endpoint_definition.pk_field_name
                )
            }
        )
        message = f"Added new {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": new_resource})


class UpdateOneToManyRelationFormView(OneToManyRelationBasedFormView):
    def dispatch(self, request, *args, **kwargs):
        self.fk_resource_id = int(self.kwargs["fk_resource_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.fk_api_client.update(self.fk_resource_id, form.cleaned_data)
        message = f"Updated {self.fk_table_name} registration."
        resource = self.fk_api_client.get(self.fk_resource_id)
        resource.update(
            {"pk": resource.get(self.fk_api_client.endpoint_definition.pk_field_name)}
        )
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource})


class DeleteOneToManyRelationFormView(OneToManyRelationView, FormView):
    form_class = ResourceDeletionForm

    def dispatch(self, request, *args, **kwargs):
        self.fk_resource_id = int(self.kwargs["fk_resource_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def form_valid(self, form):
        self.fk_api_client.delete(self.fk_resource_id)
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"result": "success"})


class EditorOverviewTemplateView(EditorTocTemplateView, TemplateView):
    template_name = "editor/overview.html"

    api_client: ApiClient
    resource_type_readable: str

    def format_resource_data_for_template(self) -> dict:
        formatted_resource_data = dict()
        column_metadata_by_column_name = dict(
            (cm.get("column_name"), cm) for cm in self.column_metadata
        )
        user_specifiable_fields = (
            self.api_client.endpoint_definition.get_all_user_specifiable_fields()
        )
        for field_name, field_metadata in user_specifiable_fields.items():
            value = self.resource.get(field_name)
            extra_metadata = column_metadata_by_column_name.get(field_name)
            field_title = field_name.replace("_", " ").title()
            field_category = UNCATEGORISED_CATEGORY
            if extra_metadata:
                field_title = extra_metadata.get("title")
                field_category = extra_metadata.get("category")
            if field_category not in formatted_resource_data:
                formatted_resource_data.update({field_category: dict()})
            formatted_resource_data[field_category].update(
                {
                    field_name: {
                        "title": field_title,
                        "value": value,
                    }
                }
            )
        return formatted_resource_data

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": f"{self.resource_type_readable.title()} {self.resource_id} | Overview",
                "main_heading": "Overview",
                "main_subheading": f"{self.resource_type_readable.title()}",
                "resource_data_by_category": self.format_resource_data_for_template(),
                "resource": self.resource,
            }
        )
        return context

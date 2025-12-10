import logging
from http import HTTPStatus

from django import forms
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from resource_management.forms import ResourceDeletionForm

from .api.base_api_clients import ApiClient, ColumnMetadataApiClient
from .api.mocks.mock_base_api_clients import MockApiClient, MockColumnMetadataApiClient
from .forms.base_forms import (
    SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix,
    SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix,
)

logger = logging.getLogger(__name__)


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
        self.column_metadata = self.column_metadata_api_client.get_resources()
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
        processed_categories = set()

        def add_category_descendents(
            category: str, category_data: dict, parent_category: str = ""
        ):
            if category in processed_categories:
                return
            processed_categories.add(category)
            if category not in category_data:
                category_data.update(
                    {
                        category: {
                            "title": category,
                            "non_toc_title": category.replace(":", ": "),
                            "descendents": dict(),
                        },
                    }
                )
                if parent_category:
                    category_data[category].update(
                        {
                            "title": category.replace(f"{parent_category}:", ""),
                        }
                    )

            category_with_colon = f"{category}:"
            descendent_names = [
                possible_descendent_name
                for possible_descendent_name in self.category_names
                if (
                    category in possible_descendent_name
                    and category != possible_descendent_name
                    and ":"
                    not in possible_descendent_name.replace(category_with_colon, "")
                )
            ]
            for dn in descendent_names:
                add_category_descendents(
                    dn, category_data[category]["descendents"], parent_category=category
                )

        self.categories = dict()
        for category in self.category_names:
            add_category_descendents(category, self.categories)

        property_names = set(
            self.api_client.endpoint_definition.get_all_user_specifiable_fields().keys()
        )
        uncategorised_property_names = self.column_names - property_names
        if uncategorised_property_names:
            self.category_names.append("Uncategorised")
            self.categories.update(
                {
                    "Uncategorised": {
                        "title": "Uncategorised",
                        "non_toc_title": "Uncategorised",
                        "descendents": dict(),
                    }
                }
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
    id_field: str
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
            kwargs={"resource_id": new_resource.get(self.id_field)},
        )
        return super().form_valid(form)


class EditorForeignKeyFormsView(TemplateView):
    resource: dict
    resource_id: int
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    editor_reverse_base: str

    def get_one_to_one_forms(self) -> dict:
        one_to_one_forms = dict()
        one_to_one_fields = (
            self.api_client.endpoint_definition.get_user_specifiable_one_to_one_fields()
        )
        for field_name, field_metadata in one_to_one_fields.items():
            fk_table_name = field_metadata.get("fk_table_name", "")
            fk_api_client = MockApiClient.get_client_instance_by_endpoint(fk_table_name)
            if not fk_api_client:
                continue
            new_form = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix(
                fk_api_client,
                MockColumnMetadataApiClient(),
                id_prefix="new",
            )
            initial = dict()
            fk_resource_id = self.resource.get(field_name)
            if fk_resource_id:
                existing_resource = fk_api_client.get(fk_resource_id)
                initial = existing_resource
            one_to_one_forms.update(
                {
                    field_name: {
                        "new_form": new_form,
                        "update_form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                            fk_api_client,
                            MockColumnMetadataApiClient(),
                            id_suffix=f"{fk_table_name}_{self.resource_id}",
                            initial=initial,
                        ),
                        "delete_form": ResourceDeletionForm(
                            initial={"resource_id_to_delete": fk_resource_id}
                        ),
                    },
                }
            )
        return one_to_one_forms

    def get_one_to_many_forms(self) -> dict:
        one_to_many_forms = dict()
        one_to_many_fields = self.api_client.endpoint_definition.get_user_specifiable_one_to_many_fields()
        for field_name, field_metadata in one_to_many_fields.items():
            fk_table_name = field_metadata.get("fk_table_name", "")
            fk_api_client = MockApiClient.get_client_instance_by_endpoint(fk_table_name)
            if not fk_api_client:
                continue
            new_form = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix(
                fk_api_client,
                MockColumnMetadataApiClient(),
                id_prefix="new",
            )
            existing_resources = fk_api_client.get_resources_referencing_resource_id(
                field_metadata.get("fk_table_column_name"), self.resource_id
            )
            one_to_many_forms.update(
                {
                    field_name: {
                        "new_form": new_form,
                        "existing_resources": {
                            existing_resource.get(
                                fk_api_client.endpoint_definition.id_field
                            ): {
                                "update_form": SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
                                    fk_api_client,
                                    MockColumnMetadataApiClient(),
                                    id_suffix=f"{fk_table_name}_{fk_api_client.endpoint_definition.id_field}",
                                    initial=existing_resource,
                                ),
                                "delete_form": ResourceDeletionForm(
                                    initial={
                                        "resource_id_to_delete": existing_resource.get(
                                            fk_api_client.endpoint_definition.id_field
                                        )
                                    }
                                ),
                            }
                            for existing_resource in existing_resources
                        },
                    },
                }
            )
        return one_to_many_forms


class EditorProcessFormView(
    EditorTocTemplateView, EditorForeignKeyFormsView, FormView, TemplateView
):
    template_name = "editor/editor_base_new.html"
    form_class: forms.Form

    api_client: ApiClient
    editor_reverse_base: str
    editor_overview_reverse_base: str
    resource_type_readable: str

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)

    def dispatch(self, request, *args, **kwargs):
        self.category = self.request.GET.get("category", self._get_first_category())
        self.success_url = reverse_lazy(
            self.editor_overview_reverse_base,
            kwargs={
                "resource_id": self.resource_id,
            },
        )
        self.title_base = f"{self.resource_type_readable.title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        one_to_one_forms = self.get_one_to_one_forms()
        one_to_many_forms = self.get_one_to_many_forms()
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title_base,
                "main_subheading": self.resource_type_readable.title(),
                "main_heading": self.title_base,
                "current_category": self.category,
                "resource": self.resource,
                "resource_id": self.resource_id,
                "one_to_one_forms": one_to_one_forms,
                "one_to_many_forms": one_to_many_forms,
            }
        )
        return context

    # Form view
    def form_valid(self, form):
        update_data = form.cleaned_data
        try:
            self.api_client.update(self.resource_id, update_data)
        except Exception:
            error_msg = f"An error occurred whilst updating {self.resource_type_readable} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.form_invalid(form)

        message = f"Updated {self.category}"
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
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
            return super().form_invalid(form)
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


class OneToOneRelationView(View):
    form_class = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)
        self.fk_column_name = self.kwargs["fk_column_name"]
        one_to_one_fields = self.api_client.endpoint_definition._get_one_to_one_fields()
        self.fk_table_name = one_to_one_fields.get(self.fk_column_name, {}).get(
            "fk_table_name"
        )
        self.fk_api_client = MockApiClient.get_client_instance_by_endpoint(
            self.fk_table_name
        )
        return super().dispatch(request, *args, **kwargs)


class OneToOneRelationBasedFormView(OneToOneRelationView, FormView):
    def form_invalid(self, form):
        messages.error(self.request, "The form submitted was not valid.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": MockApiClient.get_client_instance_by_endpoint(
                    self.fk_table_name
                ),
                "column_metadata_api_client": MockColumnMetadataApiClient(),
                "id_prefix": "new",
            }
        )
        return kwargs


class NewOneToOneRelationFormView(OneToOneRelationBasedFormView):
    def form_valid(self, form):
        new_resource = self.fk_api_client.register(form.cleaned_data)
        self.api_client.update(
            self.resource_id,
            {
                self.fk_column_name: new_resource.get(
                    self.fk_api_client.endpoint_definition.id_field
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
        fk_resource_id = self.resource.get(self.fk_column_name)
        self.fk_api_client.update(fk_resource_id, form.cleaned_data)
        message = f"Updated {self.fk_table_name} registration."
        resource = self.fk_api_client.get(fk_resource_id)
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource})


class DeleteOneToOneRelationFormView(OneToOneRelationView, FormView):
    form_class = ResourceDeletionForm

    def form_valid(self, form):
        fk_resource_id = self.resource.get(self.fk_column_name)
        self.fk_api_client.delete(fk_resource_id)
        self.api_client.update(self.resource_id, {self.fk_column_name: None})
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({})


class OneToManyRelationView(View):
    form_class = SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix
    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)
        self.fk_column_name = self.kwargs["fk_column_name"]
        self.fk_resource_id = self.kwargs["fk_resource_id"]
        one_to_many_fields = (
            self.api_client.endpoint_definition._get_one_to_many_fields()
        )
        self.fk_table_name = one_to_many_fields.get(self.fk_column_name, {}).get(
            "fk_table_name"
        )
        self.fk_table_column_name = one_to_many_fields.get(self.fk_column_name, {}).get(
            "fk_table_column_name"
        )
        self.fk_api_client = MockApiClient.get_client_instance_by_endpoint(
            self.fk_table_name
        )
        return super().dispatch(request, *args, **kwargs)


class OneToManyRelationBasedFormView(OneToManyRelationView, FormView):
    def form_invalid(self, form):
        messages.error(self.request, "The form submitted was not valid.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": MockApiClient.get_client_instance_by_endpoint(
                    self.fk_table_name
                ),
                "column_metadata_api_client": MockColumnMetadataApiClient(),
                "id_prefix": "new",
            }
        )
        return kwargs


class NewOneToManyRelationFormView(OneToManyRelationBasedFormView):
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        cleaned_data.update({self.fk_table_column_name: self.resource_id})
        new_resource = self.fk_api_client.register(cleaned_data)
        message = f"Added new {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": new_resource})


class UpdateOneToManyRelationFormView(OneToManyRelationBasedFormView):
    def form_valid(self, form):
        self.fk_api_client.update(self.fk_resource_id, form.cleaned_data)
        message = f"Updated {self.fk_table_name} registration."
        resource = self.fk_api_client.get(self.fk_resource_id)
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource})


class DeleteOneToManyRelationFormView(OneToManyRelationView, FormView):
    form_class = ResourceDeletionForm

    def form_valid(self, form):
        self.fk_api_client.delete(self.fk_resource_id)
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({})


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
            field_category = "Uncategorised"
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

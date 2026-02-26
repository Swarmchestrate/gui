import asyncio
import logging
from http import HTTPStatus

from django import forms
from django.http import JsonResponse
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
from .services import get_categories_for_editor, prepare_initial_form_data


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
                "category_names": self.category_names,
                "initial_category": self.category,
            }
        )
        return context


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
                initial = prepare_initial_form_data(existing_resource)
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
                                    initial=prepare_initial_form_data(
                                        existing_resource
                                    ),
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
        return JsonResponse(
            {
                "message": message,
                "redirect": self.success_url,
            }
        )

    def form_invalid(self, form):
        error_msg = (
            "Some fields were invalid. Please apply fixes for the highlighted fields."
        )
        return JsonResponse(
            {
                "feedback": error_msg,
                "url": self.request.get_full_path(),
            },
            status=HTTPStatus.BAD_REQUEST,
        )


class EditorTabbedFormTemplateView(
    EditorFormView,
    EditorForeignKeyFieldsTemplateView,
    EditorTocTemplateView,
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
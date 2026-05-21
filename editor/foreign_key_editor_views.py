from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View
from http import HTTPStatus

from .forms import (
    ForeignKeyFormWithDynamicallyPopulatedFields,
    FormWithDynamicallyPopulatedFields,
)
from .view_helpers import EditorTableOfContents, get_form_config_for_table
from postgrest.api import ApiClient, Resource
from postgrest.forms.form_config import FormConfig
from postgrest.table_names import TableNames
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_resource_type


class EditorBasedOneToOneFieldView(View):
    table_name: str

    new_one_to_one_relation_editor_reverse_base: str
    update_one_to_one_relation_editor_reverse_base: str
    delete_one_to_one_relation_editor_reverse_base: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = kwargs["resource_id"]
        self.fk_column_name = self.kwargs["fk_column_name"]
        # API client is instantiated here so it doesn't
        # fetch the OpenAPI spec twice.
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        definition = self.api_client.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        self.form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata,
            infer_one_to_many_properties=True,
            disabled_properties=[
                TableNames.APPLICATION,
                TableNames.APPLICATION_NEW,
                TableNames.APPLICATION_MICROSERVICE,
                TableNames.CAPACITY,
                TableNames.CAPACITY_NEW,
            ]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_fk_resource(self):
        # Get the main resource
        endpoint = self.api_client.get_endpoint(self.table_name)
        resource = endpoint.get(self.resource_id)
        # Get the other resource that is referenced
        # by the main resource (if any).
        fk_table_endpoint = self.api_client.get_endpoint(self.fk_table_name)
        fk_resource_id = resource.as_dict().get(self.fk_column_name)
        if not fk_resource_id:
            return None
        return fk_table_endpoint.get(fk_resource_id)
    
    def get_section_template(self, fk_resource: Resource):
        initial = dict()
        if fk_resource:
            initial = fk_resource.as_dict()
        return render_to_string("editor/foreign_key_fields_new/editor_based/one_to_one_field_section.html", {
            "field_name": self.fk_column_name,
            "resource": self.get_fk_resource(),
            "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                fields=self.form_config.get_fields(),
                initial=initial
            ),
            "resource_type": self.fk_table_name,
        })

    def get(self, request, *args, **kwargs):
        fk_resource = self.get_fk_resource()
        return JsonResponse({
            "section": self.get_section_template(fk_resource),
        })


class EditorBasedOneToManyFieldView(View):
    table_name: str
    resource_type: str

    new_one_to_many_relation_reverse_base: str
    update_one_to_many_relation_reverse_base: str
    delete_one_to_many_relation_reverse_base: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_table_name = self.kwargs["fk_column_name"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        openapi_spec = self.api_client.openapi_spec
        if not hasattr(self, "possible_fk_table_column_name"):
            self.possible_fk_table_column_name = f"{self.table_name}_id"
        referring_tables = openapi_spec.find_references_to_table(
            self.table_name,
            possible_column_name=self.possible_fk_table_column_name
        )
        self.fk_table_column_name = referring_tables.get(self.fk_table_name)
        if not self.fk_table_column_name:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        self.form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata,
            infer_one_to_many_properties=True,
            disabled_properties=[
                f"{TableNames.APPLICATION}_id",
                f"{TableNames.APPLICATION_NEW}_id",
                f"{TableNames.APPLICATION_MICROSERVICE}_id",
                f"{TableNames.CAPACITY}_id",
                f"{TableNames.CAPACITY_NEW}_id",
            ]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_resources(self) -> list[Resource]:
        # Get resources referring to the main resources.
        fk_table_endpoint = self.api_client.get_endpoint(self.fk_table_name)
        return fk_table_endpoint.get_resources_referencing_resource_id(
            self.fk_table_column_name,
            self.resource_id
        )

    def get_section_template(self, forms_for_existing_fk_resources: dict):
        return render_to_string("editor/foreign_key_fields_new/editor_based/one_to_many_field_section.html", {
            "resource_id": self.resource_id,
            "field_name": self.fk_table_name,
            "forms_for_existing_resources": forms_for_existing_fk_resources,
            "resource_type": self.fk_table_name,
            "new_editor_reverse_base": self.new_editor_reverse_base,
        })

    def get_list_item_template(self):
        return render_to_string(
            "editor/foreign_key_fields_new/editor_based/one_to_many_field_list_item.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_suffix="__resource_id__",
                ),
                "resource_id": "__resource_id__",
                "resource_type": self.fk_table_name,
                "field": {"name": self.fk_table_name},
                "field_name": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        fk_resources = self.get_resources()
        return JsonResponse({
            "section": self.get_section_template({
                fk_resource.pk: {
                    "delete_form": self.get_delete_form(fk_resource.pk),
                }
                for fk_resource in fk_resources
            }),
        })


class NestedForeignKeyResourceEditorView(TemplateView):
    template_name = "editor/nested_editors/new_editor.html"

    table_name: str
    column_metadata_table_name: str
    disabled_categories: list[str]
    disabled_properties: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_table_name = self.kwargs["fk_column_name"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        if not hasattr(self, "disabled_properties"):
            self.disabled_properties = list()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories,
            disabled_properties=[
                TableNames.APPLICATION,
                TableNames.APPLICATION_NEW,
                TableNames.CAPACITY,
                TableNames.CAPACITY_NEW,
                *self.disabled_properties,
            ]
        )
        self.fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_categories=self.disabled_categories,
            disabled_properties=[
                TableNames.APPLICATION,
                TableNames.APPLICATION_NEW,
                TableNames.CAPACITY,
                TableNames.CAPACITY_NEW,
                *self.disabled_properties,
            ]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_forms_by_category(
            self,
            form_config: FormConfig,
            initial: dict | None = None):
        forms_by_category = dict()
        for category in form_config.get_field_categories():
            if category in self.disabled_categories:
                continue
            if not category:
                forms_by_category.update({
                UNKNOWN_ATTRIBUTE_CATEGORY: FormWithDynamicallyPopulatedFields(
                        fields=form_config.get_fields_for_category(category),
                        initial=self.resource.as_dict(),
                    )
                })
                continue
            forms_by_category.update({
                category: FormWithDynamicallyPopulatedFields(
                    fields=form_config.get_fields_for_category(category),
                    initial=self.resource.as_dict(),
                )
            })
        return forms_by_category

    def get_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        return EditorTableOfContents(
            self.table_name,
            category_names,
            is_unknown_category_needed=any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in self.form_config.get_fields().values()
            )
        ).as_dict()

    def get_fk_table_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.fk_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        return EditorTableOfContents(
            self.fk_table_name,
            category_names,
            is_unknown_category_needed=any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in self.fk_table_form_config.get_fields().values()
            )
        ).as_dict()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update({
            "title": f"{humanise_resource_type(self.resource_type).title()} {self.resource_id} | Overview",
            "main_subheading": humanise_resource_type(self.resource_type).title(),
            "main_heading": f"New {humanise_resource_type(self.fk_table_name).title()}",
            "resource": self.resource.as_dict(),
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_one_to_one_section_reverse_base": self.editor_one_to_one_section_reverse_base,
            "editor_one_to_many_section_reverse_base": self.editor_one_to_many_section_reverse_base,
            "toc_list_items": self.get_toc_list_items(),
            "nested_toc_list_items": self.get_fk_table_toc_list_items(),
            "forms_by_category": self.get_forms_by_category(self.fk_table_form_config),
        })
        return context
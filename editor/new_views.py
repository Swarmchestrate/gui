import logging
import lxml.html
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from postgrest.api_clients import ColumnMetadataApiClient
from postgrest.base.base_api_clients import ApiClient
from postgrest.forms.form_config import (
    FormConfig,
    PropertiesMetadata,
)
from postgrest.forms.foreign_key_fields import (
    get_foreign_key_form_configs,
    get_one_to_many_field_forms,
    get_one_to_one_field_forms,
)

# from postgrest.mocks.base.mock_base_api_clients import MockApiClient as ApiClient
# from postgrest.mocks.mock_api_clients import (
#     MockColumnMetadataApiClient as ColumnMetadataApiClient,
# )

from .forms.base_forms import FormWithDynamicallyPopulatedFields
from .services import get_categories_for_editor


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


class EditorTabbedFormTemplateView(
    EditorTocTemplateView,
    TemplateView,
):
    template_name = "editor/editor_tab.html"
    categorised_form_class = FormWithDynamicallyPopulatedFields

    new_one_to_one_relation_reverse_base: str
    update_one_to_one_relation_reverse_base: str
    delete_one_to_one_relation_reverse_base: str
    new_one_to_many_relation_reverse_base: str
    update_one_to_many_relation_reverse_base: str
    delete_one_to_many_relation_reverse_base: str

    editor_form_reverse: str
    editor_form_url: str

    def initialise_categorised_forms(self):
        properties_metadata = PropertiesMetadata(
            "capacity_new",
            self.openapi_spec,
            self.column_metadata,
            column_metadata_table_name="capacity"
        )
        self.properties_metadata = dict()
        categorised_properties_metadata = properties_metadata.as_categorised_dict()
        for properties_metadata in categorised_properties_metadata.values():
            self.properties_metadata.update(properties_metadata)
        self.forms_by_category = {
            category: FormWithDynamicallyPopulatedFields(
                FormConfig(properties_metadata).get_fields(),
                initial=self.resource,
            )
            for category, properties_metadata in categorised_properties_metadata.items()
        }
        

    def initialise_one_to_one_field_forms(self):
        properties_by_fk_tables = dict()
        for property_name, property_metadata in self.properties_metadata.items():
            try:
                xpath_results = lxml.html.fromstring(property_metadata.description).xpath("fk/@table")
            except TypeError:
                continue
            fk_table_name = next(iter(xpath_results), None)
            if not fk_table_name:
                continue
            if fk_table_name not in properties_by_fk_tables:
                properties_by_fk_tables.update({
                    fk_table_name: [],
                })
            properties_by_fk_tables[fk_table_name].append(property_name)
        form_configs = get_foreign_key_form_configs(
            properties_by_fk_tables.keys(),
            self.openapi_spec,
            self.column_metadata
        )
        self.one_to_one_field_metadata = get_one_to_one_field_forms(
            self.resource,
            form_configs,
            properties_by_fk_tables
        )
    
    def initialise_one_to_many_field_forms(self):
        definitions = self.openapi_spec.get("definitions", {})
        table_names = list()
        for definition_name, definition in definitions.items():
            if 'capacity_id' not in definition.get("properties", {}):
                continue
            table_names.append(definition_name)
        form_configs = get_foreign_key_form_configs(
            table_names,
            self.openapi_spec,
            self.column_metadata
        )
        # Check each definition for references to the references to the main form type.
        # E.g., a property is called "capacity_id" or "application_id", or, there is
        # an explicit "@fk_table_name" expression. E.g. fk_table_name="capacity".
        self.one_to_many_field_metadata = get_one_to_many_field_forms(
            self.request,
            self.resource_id,
            form_configs,
            self.update_one_to_many_relation_reverse_base,
            self.delete_one_to_many_relation_reverse_base
        )

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.api_client.get(self.resource_id)

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        self.title_base = f"{self.resource_type_readable.title()} {self.resource_id}"
        self.editor_form_url = reverse_lazy(
            self.editor_form_reverse, kwargs={"resource_id": self.resource_id}
        )
        self.openapi_spec = self.api_client.get_openapi_spec()
        self.column_metadata = self.column_metadata_api_client.get_resources()
        self.initialise_categorised_forms()
        self.initialise_one_to_one_field_forms()
        self.initialise_one_to_many_field_forms()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "resource": self.resource,
                "resource_id": self.resource_id,
                "initial_category": self.category,
                "forms_by_category": self.forms_by_category,
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
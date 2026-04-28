import json
import logging
import lxml.html
from http import HTTPStatus

from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
)

from .new_forms import FormWithDynamicallyPopulatedFields
from .view_helpers import EditorTableOfContents

from postgrest.new_api import (
    ApiClient,
    OpenApiSpecification,
)
from postgrest.forms.foreign_key_fields import (
    get_foreign_key_form_configs,
    get_one_to_many_field_forms,
    get_one_to_one_field_forms,
)
from postgrest.forms.form_config import (
    FormConfig,
    Properties,
)
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY


logger = logging.getLogger(__name__)


class EditorSkeletonLoaderView(TemplateView):
    template_name = "editor/editor_base_tabbed.html"

    table_name: str
    editor_overview_reverse_base: str
    toc_url: str
    tabbed_form_url: str
    tabbed_form_reverse: str
    resource_type_readable: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.resource = ApiClient().get_endpoint(self.table_name).get(self.resource_id)
        self.category = request.GET.get("category", "")
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


class EditorTableOfContentsSectionView(TemplateView):
    table_name: str
    categories: dict
    disabled_categories: list
    template_name = "editor/toc_tabbed/toc_base.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_client = ApiClient()
        definition = api_client.get_endpoint(self.table_name).definition
        column_metadata = [
            resource.as_dict()
            for resource in api_client.get_endpoint("column_metadata").get_resources()
        ]
        category_names = list(set(
            resource.get("category", "")
            for resource in column_metadata
            if resource.get("table_name", "") == self.table_name
        ))
        category_names.sort()
        categories = EditorTableOfContents(
            self.table_name,
            category_names,
            column_metadata,
            definition.properties.keys()
        ).as_dict()
        context.update({
            "toc_list_items": categories,
            "initial_category": self.category,
        })
        return context


class EditorTabSectionView(TemplateView):
    template_name = "editor/editor_tab.html"
    
    table_name: str
    column_metadata_table_name: str
    openapi_spec: OpenApiSpecification

    new_one_to_one_relation_reverse_base: str
    update_one_to_one_relation_reverse_base: str
    delete_one_to_one_relation_reverse_base: str
    new_one_to_many_relation_reverse_base: str
    update_one_to_many_relation_reverse_base: str
    delete_one_to_many_relation_reverse_base: str

    editor_form_reverse: str
    editor_form_url: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.category = request.GET.get("category")
        
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        resource_endpoint = self.api_client.get_endpoint(self.table_name)
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        self.resource = resource_endpoint.get(self.resource_id)
        self.title_base = f"{resource_endpoint.resource_type.title()} {self.resource_id}"
        self.editor_form_url = reverse_lazy(
            self.editor_form_reverse, kwargs={"resource_id": self.resource_id}
        )
        self.column_metadata = column_metadata_endpoint.get_resources()
        self._properties = Properties(
            self.table_name,
            self.openapi_spec.get_definition(self.table_name),
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name
        )
        # One-to-many fields are handled first, as they are
        # added to the category-based forms before they
        # are generated.
        self.initialise_one_to_many_field_forms()
        self.initialise_categorised_forms()
        self.initialise_one_to_one_field_forms()
        self.initialise_toc_list_items()
        return super().dispatch(request, *args, **kwargs)
    
    def initialise_one_to_many_field_forms(self):
        definitions = self.openapi_spec.get_definitions()
        table_names = list()
        for definition_name, definition in definitions.items():
            # TEMP: replace foreign key criteria with presence of
            # <fk table_name="..." column_name="..."> in description
            # instead of presence of property name.
            if f'{self.column_metadata_table_name}_id' not in definition.properties:
                continue
            table_names.append(definition_name)
            self._properties.add_one_to_many_property(definition_name)
        form_configs = get_foreign_key_form_configs(
            table_names,
            self.openapi_spec,
            self.column_metadata,
            disabled_property_names=[f'{self.column_metadata_table_name}_id']
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

    def initialise_one_to_one_field_forms(self):
        properties_by_fk_tables = dict()
        for property_name, property_metadata in self.properties.items():
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

    def initialise_categorised_forms(self):
        categorised_properties = self._properties.as_categorised_dict()
        self.properties = dict()
        for properties in categorised_properties.values():
            self.properties.update(properties)
        self.forms_by_category = {
            category: FormWithDynamicallyPopulatedFields(
                fields=FormConfig(properties).get_fields(),
                initial=self.resource.as_dict(),
            )
            for category, properties in categorised_properties.items()
        }
    
    def initialise_toc_list_items(self):
        definition = self.openapi_spec.get_definition(self.table_name)
        column_metadata = [
            resource.as_dict()
            for resource in self.api_client.get_endpoint("column_metadata").get_resources()
        ]
        category_names = list(set(
            resource.get("category", "")
            for resource in column_metadata
            if resource.get("table_name", "") == self.column_metadata_table_name
        ))
        category_names.sort()
        self.toc_list_items = EditorTableOfContents(
            self.table_name,
            category_names,
            column_metadata,
            definition.properties.keys()
        ).as_dict()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "resource": self.resource,
                "resource_id": self.resource_id,
                "initial_category": self.category,
                "forms_by_category": self.forms_by_category,
                "editor_form_url": self.editor_form_url,
                "toc_list_items": self.toc_list_items,
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


class UpdateResourceByCategoryView(FormView):
    form_class = FormWithDynamicallyPopulatedFields

    openapi_spec: OpenApiSpecification
    table_name: str
    column_metadata_table_name: str
    editor_overview_reverse_base: str
    resource_type_readable: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.category = self.request.GET.get("category")
        if not self.category:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
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
            self.api_client.get_endpoint(self.table_name).update(
                self.resource_id,
                update_data
            )
        except Exception:
            error_msg = f"An error occurred whilst updating {self.resource_type_readable} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.api_invalid()

        message = f"Saved changes to {self.category.replace(':', ': ')}."
        return JsonResponse({"message": message})

    def form_invalid(self, form):
        error_msg = "Some fields were invalid. Please apply fixes for the highlighted fields."
        return JsonResponse(
            {"message": error_msg, "feedback": json.loads(form.errors.as_json())},
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
        column_metadata_endpoint = self.api_client.get_endpoint(
            "column_metadata"
        )
        properties = Properties(
            self.table_name,
            self.openapi_spec.get_definition(self.table_name),
            column_metadata_endpoint.get_resources(),
            column_metadata_table_name=self.column_metadata_table_name
        )
        kwargs.update({
            "fields": FormConfig(properties.as_dict()).get_fields_for_category(self.category),
        })
        return kwargs


class EditorStartFormView(FormView):
    form_class = FormWithDynamicallyPopulatedFields

    table_name: str
    openapi_spec: OpenApiSpecification
    editor_reverse_base: str
    resource_type_readable: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_resource = self.api_client.get_endpoint(
            self.table_name
        ).register(form.cleaned_data)
        messages.success(
            self.request,
            f"New {self.resource_type_readable} registered.",
        )
        self.success_url = reverse_lazy(
            self.editor_reverse_base,
            kwargs={"resource_id": new_resource.pk},
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        definition = self.openapi_spec.get_definition(self.table_name)
        column_metadata = [
            resource.as_dict()
            for resource in self.api_client.get_endpoint(
                "column_metadata"
            ).get_resources()
        ]
        category_names = list(set(
            resource.get("category", "")
            for resource in column_metadata
            if resource.get("table_name", "") == self.table_name
        ))
        category_names.sort()
        categories = EditorTableOfContents(
            self.table_name,
            category_names,
            column_metadata,
            definition.properties.keys()
        ).as_dict()
        context.update({
            "toc_list_items": categories,
            "title": f"New {self.resource_type_readable.title()}",
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint(
            "column_metadata"
        )
        properties = Properties(
            self.table_name,
            self.openapi_spec.get_definition(self.table_name),
            column_metadata_endpoint.get_resources()
        )
        kwargs.update({
            "fields": FormConfig(properties.as_dict()).get_required_fields(),
        })
        return kwargs


class EditorOverviewTemplateView(TemplateView):
    template_name = "editor/overview_base.html"

    table_name: str
    resource_type_readable: str

    def format_resource_data_for_template(self) -> dict:
        formatted_resource_data = dict()
        column_metadata_by_column_name = dict(
            (cm.get("column_name"), cm)
            for cm in self.column_metadata
        )
        user_specifiable_fields = self.endpoint.definition.properties
        for field_name, field_metadata in user_specifiable_fields.items():
            value = self.resource.get(field_name)
            extra_metadata = column_metadata_by_column_name.get(field_name)
            field_title = field_name.replace("_", " ").title()
            field_category = UNKNOWN_ATTRIBUTE_CATEGORY
            if extra_metadata:
                field_title = extra_metadata.get("title")
                field_category = extra_metadata.get("category")
            if field_category not in formatted_resource_data:
                formatted_resource_data.update({field_category: dict()})
            formatted_resource_data[field_category].update({
                field_name: {
                    "title": field_title,
                    "value": value,
                }
            })
        return formatted_resource_data

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.endpoint = self.api_client.get_endpoint(self.table_name)
        self.resource_id = self.kwargs["resource_id"]
        self.resource = self.endpoint.get(self.resource_id)
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

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

from .forms import FormWithDynamicallyPopulatedFields
from .view_helpers import EditorTableOfContents

from editor.view_helpers import get_form_config_for_table
from postgrest.forms.foreign_key_fields import (
    get_foreign_key_form_configs,
    get_one_to_many_field_forms,
    get_one_to_one_field_forms,
)
from postgrest.new_api import (
    ApiClient,
    OpenApiSpecification,
    Resource,
)
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_resource_type


logger = logging.getLogger(__name__)


class EditorSkeletonLoaderView(TemplateView):
    template_name = "editor/editor_base_tabbed.html"

    table_name: str
    resource_type: str

    editor_overview_reverse_base: str
    toc_url: str
    tabbed_form_url: str
    tabbed_form_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
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
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.title_base = f"{humanise_resource_type(self.resource_type).title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title_base,
                "main_subheading": humanise_resource_type(self.resource_type).title(),
                "main_heading": self.title_base,
                "resource_id": self.resource_id,
                "toc_url": self.toc_url,
                "tabbed_form_url": self.tabbed_form_url,
                "initial_category": self.category,
                "toast_template": render_to_string("editor/toast_template.html", {}),
                "resource_type": self.resource_type,
            }
        )
        return context


class EditorTableOfContentsSectionView(TemplateView):
    template_name = "editor/toc_tabbed/toc_base.html"

    table_name: str
    column_metadata_table_name: str
    disabled_categories: list[str]

    categories: dict

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_client = ApiClient()
        column_metadata = api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        form_config = get_form_config_for_table(
            self.table_name,
            api_client.openapi_spec,
            column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        form_fields = form_config.get_fields()
        toc_list_items = EditorTableOfContents(
            self.table_name,
            category_names,
            is_unknown_category_needed=any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in form_fields.values()
            )
        ).as_dict()
        context.update({
            "toc_list_items": toc_list_items,
            "initial_category": self.category,
        })
        return context


class EditorTabSectionView(TemplateView):
    template_name = "editor/editor_tab.html"
    
    table_name: str
    column_metadata_table_name: str
    openapi_spec: OpenApiSpecification
    column_metadata: list[Resource]
    referring_tables: dict[str, str]
    disabled_categories: list[str]
    resource_type: str

    editor_overview_reverse_base: str
    editor_one_to_one_section_reverse_base: str
    editor_one_to_many_section_reverse_base: str
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
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        return super().dispatch(request, *args, **kwargs)

    def get_forms_by_category(self):
        forms_by_category = dict()
        for category in self.form_config.get_field_categories():
            if category in self.disabled_categories:
                continue
            if not category:
                forms_by_category.update({
                UNKNOWN_ATTRIBUTE_CATEGORY: FormWithDynamicallyPopulatedFields(
                        fields=self.form_config.get_fields_for_category(category),
                        initial=self.resource.as_dict(),
                    )
                })
                continue
            forms_by_category.update({
                category: FormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields_for_category(category),
                    initial=self.resource.as_dict(),
                )
            })
        return forms_by_category
    
    def get_toc_list_items(self):
        column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        form_fields = self.form_config.get_fields()
        return EditorTableOfContents(
            self.table_name,
            category_names,
            is_unknown_category_needed=any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in form_fields.values()
            )
        ).as_dict()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update(
            {
                "resource": self.resource,
                "resource_id": self.resource_id,
                "initial_category": self.category,
                "toc_list_items": self.get_toc_list_items(),
                "forms_by_category": self.get_forms_by_category(),
                "editor_form_url": self.editor_form_url,
                "resource_type": self.resource_type,
                "editor_overview_reverse_base": self.editor_overview_reverse_base,
                "editor_one_to_one_section_reverse_base": self.editor_one_to_one_section_reverse_base,
                "editor_one_to_many_section_reverse_base": self.editor_one_to_many_section_reverse_base,
            }
        )
        return context


class EditorView(TemplateView):
    table_name: str
    column_metadata_table_name: str
    openapi_spec: OpenApiSpecification
    column_metadata: list[Resource]
    referring_tables: dict[str, str]
    disabled_categories: list[str]
    resource_type: str

    editor_overview_reverse_base: str
    editor_one_to_one_section_reverse_base: str
    editor_one_to_many_section_reverse_base: str
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
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        self.title_base = f"{humanise_resource_type(self.resource_type).title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)
    
    def get_toc_list_items(self):
        column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        form_fields = self.form_config.get_fields()
        return EditorTableOfContents(
            self.table_name,
            category_names,
            is_unknown_category_needed=any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in form_fields.values()
            )
        ).as_dict()

    def get_forms_by_category(self):
        forms_by_category = dict()
        for category in self.form_config.get_field_categories():
            if category in self.disabled_categories:
                continue
            if not category:
                forms_by_category.update({
                UNKNOWN_ATTRIBUTE_CATEGORY: FormWithDynamicallyPopulatedFields(
                        fields=self.form_config.get_fields_for_category(category),
                        initial=self.resource.as_dict(),
                    )
                })
                continue
            forms_by_category.update({
                category: FormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields_for_category(category),
                    initial=self.resource.as_dict(),
                )
            })
        return forms_by_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update(
            {
                "title": self.title_base,
                "main_subheading": humanise_resource_type(self.resource_type).title(),
                "main_heading": self.title_base,
                "resource": self.resource,
                "resource_id": self.resource_id,
                "initial_category": self.category,
                "resource_type": self.resource_type,
                "editor_form_url": self.editor_form_url,
                "editor_overview_reverse_base": self.editor_overview_reverse_base,
                "editor_one_to_one_section_reverse_base": self.editor_one_to_one_section_reverse_base,
                "editor_one_to_many_section_reverse_base": self.editor_one_to_many_section_reverse_base,
                "toc_list_items": self.get_toc_list_items(),
                "forms_by_category": self.get_forms_by_category(),
                "toast_template": render_to_string("editor/toast_template.html", {}),
            }
        )
        return context


class UpdateResourceByCategoryView(FormView):
    form_class = FormWithDynamicallyPopulatedFields

    openapi_spec: OpenApiSpecification
    table_name: str
    column_metadata_table_name: str
    disabled_categories: list[str]
    
    editor_overview_reverse_base: str
    resource_type: str

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
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        self.success_url = reverse_lazy(
            self.editor_overview_reverse_base,
            kwargs={
                "resource_id": self.resource_id,
            },
        )
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.title_base = f"{humanise_resource_type(self.resource_type).title()} {self.resource_id}"
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        update_data = form.cleaned_data
        try:
            self.api_client.get_endpoint(self.table_name).update(
                self.resource_id,
                update_data
            )
        except Exception:
            error_msg = f"An error occurred whilst updating {humanise_resource_type(self.resource_type)} {self.resource_id}. The update may not have been applied."
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
                "message": f"An error occurred whilst updating {humanise_resource_type(self.resource_type)} {self.resource_id}. The update may not have been applied.",
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            column_metadata_endpoint.get_resources(),
            infer_one_to_many_properties=False,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        if self.category == UNKNOWN_ATTRIBUTE_CATEGORY:
            kwargs.update({
                "fields": form_config.get_fields_for_category(None),
            })
            return kwargs
        kwargs.update({
            "fields": form_config.get_fields_for_category(self.category),
        })
        return kwargs


class EditorStartFormView(FormView):
    form_class = FormWithDynamicallyPopulatedFields

    table_name: str
    column_metadata_table_name: str
    openapi_spec: OpenApiSpecification
    disabled_categories: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_resource = self.api_client.get_endpoint(
            self.table_name
        ).register(form.cleaned_data)
        messages.success(
            self.request,
            f"New {humanise_resource_type(self.resource_type)} registered.",
        )
        self.success_url = reverse_lazy(
            self.editor_reverse_base,
            kwargs={"resource_id": new_resource.pk},
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("category", "") not in self.disabled_categories)
        ))
        category_names.sort()
        categories = EditorTableOfContents(
            self.table_name,
            category_names,
            is_unknown_category_needed=False
        ).as_dict()
        context.update({
            "toc_list_items": categories,
            "title": f"New {humanise_resource_type(self.resource_type).title()}",
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "fields": self.form_config.get_required_fields(),
        })
        return kwargs


class EditorOverviewTemplateView(TemplateView):
    template_name = "editor/overview_base.html"

    table_name: str
    column_metadata_table_name: str
    disabled_categories: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_categories"):
            self.disabled_categories = list()
        form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_categories=self.disabled_categories
        )
        self.properties_as_dict = form_config.get_properties()
        self.form_fields = form_config.get_fields()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)
    
    def get_toc(self):
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
                for field in self.form_fields.values()
            )
        ).as_dict()

    def format_resource_data_for_template(self) -> dict:
        formatted_resource_data = dict()
        for property_name, metadata in self.properties_as_dict.items():
            if property_name not in self.form_fields:
                continue
            value = self.resource.as_dict().get(property_name)
            field_title = metadata.title
            if not field_title:
                field_title = " ".join(property_name.split("_")).title()
            field_category = metadata.category
            if not field_category:
                field_category = UNKNOWN_ATTRIBUTE_CATEGORY
            if field_category not in formatted_resource_data:
                formatted_resource_data.update({field_category: dict()})
            formatted_resource_data[field_category].update({
                property_name: {
                    "title": field_title,
                    "value": value,
                }
            })
        return formatted_resource_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": f"{humanise_resource_type(self.resource_type).title()} {self.resource_id} | Overview",
                "main_heading": "Overview",
                "main_subheading": f"{humanise_resource_type(self.resource_type).title()}",
                "resource_data_by_category": self.format_resource_data_for_template(),
                "resource": self.resource.as_dict(),
                "toc_list_items": self.get_toc(),
                "editor_reverse_base": self.editor_reverse_base,
            }
        )
        return context

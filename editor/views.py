import logging
from http import HTTPStatus

from django import forms
from django.contrib import messages
from django.forms import Form, formset_factory
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
)
from django.views.generic.edit import ProcessFormView

from .api.base_api_clients import ApiClient, ColumnMetadataApiClient
from .base_formsets import BaseEditorFormSet

logger = logging.getLogger(__name__)


class UncategorisedEditorTemplateView(TemplateView):
    api_client: ApiClient


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
        return next(iter(self.category_names))

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


class EditorRouterView(EditorTocTemplateView, ProcessFormView):
    editor_view_class: TemplateView
    uncategorised_editor_view_class: TemplateView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "uncategorised":
            return self.uncategorised_editor_view_class.as_view()(
                request, *args, **kwargs
            )
        return self.editor_view_class.as_view()(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.route_to_view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.route_to_view(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.category = self.request.GET.get("category", self._get_first_category())
        return super().dispatch(request, *args, **kwargs)


class EditorProcessFormView(EditorTocTemplateView, FormView, TemplateView):
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
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title_base,
                "main_subheading": self.resource_type_readable.title(),
                "main_heading": self.title_base,
                "current_category": self.category,
                "resource": self.resource,
                "resource_id": self.resource_id,
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


class MultipleEditorFormsetProcessFormView(EditorProcessFormView):
    formset_classes: dict
    initial_data_for_formsets: dict[str, list[dict]]
    manually_processed_formset_prefixes: set[str]
    formsets_not_using_table_templates: set[str]

    # Class-specific methods
    def add_formset_class(
        self,
        form_class: Form,
        formset_prefix: str,
        base_formset_class: BaseEditorFormSet = None,
        can_delete: bool | None = None,
        extra_formset_factory_kwargs: dict | None = None,
        add_to_main_form: bool = True,
    ):
        if not base_formset_class:
            base_formset_class = BaseEditorFormSet
        if can_delete is None:
            can_delete = True
        if not extra_formset_factory_kwargs:
            extra_formset_factory_kwargs = dict()
        formset_class = formset_factory(
            form_class,
            formset=base_formset_class,
            can_delete=can_delete,
            **extra_formset_factory_kwargs,
        )
        self.formset_classes.update({formset_prefix: formset_class})
        if add_to_main_form:
            return
        self.manually_processed_formset_prefixes.add(formset_prefix)

    def add_initial_data_for_formset(self, data: list[dict], formset_prefix: str):
        self.initial_data_for_formsets.update({formset_prefix: data})

    def get_initial_data_for_formset(self, formset_prefix: str):
        return self.initial_data_for_formsets.get(formset_prefix, list())

    def exclude_formset_from_table_templates(self, formset_prefix: str):
        return self.formsets_not_using_table_templates.add(formset_prefix)

    # EditorProcessFormView method overrides
    def get_forms_from_request_data(self, request):
        forms = super().get_forms_from_request_data(request)
        for formset_prefix, formset_class in self.formset_classes.items():
            initial = self.get_initial_data_for_formset(formset_prefix)
            loaded_formset = formset_class(
                data=request.POST, initial=initial, prefix=formset_prefix
            )
            forms.update({formset_prefix: loaded_formset})
        return forms

    def get_context_data_forms_invalid(self, forms):
        context = super().get_context_data_forms_invalid(forms)
        for form_prefix, formset in forms.items():
            context.update(
                {
                    f"{form_prefix}_formset": formset,
                }
            )
        return context

    def add_formset_data_to_main_form(self, cleaned_data: dict, forms: dict):
        cleaned_data = super().add_formset_data_to_main_form(cleaned_data, forms)
        for formset_prefix, formset in forms.items():
            if not formset_prefix:
                continue
            if formset_prefix in self.manually_processed_formset_prefixes:
                # The property will be updated when the
                # formset is processed after the main form.
                cleaned_data.pop(formset_prefix, None)
                continue
            formset_data = formset.to_api_ready_format()
            cleaned_data.update(
                {
                    formset_prefix: formset_data,
                }
            )
        return cleaned_data

    # ProcessFormView method overrides
    def setup(self, request, *args, **kwargs):
        self.initial_data_for_formsets = dict()
        self.formset_classes = dict()
        self.manually_processed_formset_prefixes = set()
        self.formsets_not_using_table_templates = set()
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for formset_prefix, formset_class in self.formset_classes.items():
            initial = self.get_initial_data_for_formset(formset_prefix)
            initial_formset = formset_class(initial=initial, prefix=formset_prefix)
            if "formsets" not in context:
                context.update({"formsets": dict()})
            context.update({f"{formset_prefix}_formset": initial_formset})
            context["formsets"].update({formset_prefix: initial_formset})
            if formset_prefix in self.formsets_not_using_table_templates:
                continue
            if "formset_tables" not in context:
                context.update({"formset_tables": dict()})
            context.update({f"{formset_prefix}_formset": initial_formset})
            context["formset_tables"].update({formset_prefix: initial_formset})
        return context


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

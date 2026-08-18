from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import FormView

from .forms import FormWithDynamicallyPopulatedFields
from .view_helpers import EditorTableOfContents, get_form_config_for_table
from postgrest.api import ApiClient
from postgrest.forms.form_config import FormConfig
from postgrest.table_names import TableNames
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_resource_type, resource_label


class OneToManyForeignKeyResourceEditorView(FormView):
    form_class = FormWithDynamicallyPopulatedFields
    template_name = "editor/editor_for_foreign_key_fields/fk_update_editor.html"
    success_reverse_base: str

    table_name: str
    column_metadata_table_name: str
    disabled_properties: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_table_name = self.kwargs["fk_table_name"]
        self.fk_resource_id = self.kwargs["fk_resource_id"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_properties"):
            self.disabled_properties = list()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_properties=self.disabled_properties
        )
        self.category = self.form_config.get_fields().get(
            self.fk_table_name
        ).category
        self.fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=self.disabled_properties
        )
        return super().dispatch(request, *args, **kwargs)

    def get_forms_by_category(
            self,
            form_config: FormConfig,
            initial: dict | None = None):
        forms_by_category = dict()
        for category in form_config.get_field_categories():
            form_for_category = FormWithDynamicallyPopulatedFields(
                fields=form_config.get_fields_for_category(category),
                initial=initial
            )
            if not category:
                forms_by_category.update({
                    UNKNOWN_ATTRIBUTE_CATEGORY: form_for_category,
                })
                continue
            forms_by_category.update({
                category: form_for_category,
            })
        return forms_by_category

    def get_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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

    def form_valid(self, form):
        update_data = form.cleaned_data
        fk_table_definition = self.openapi_spec.get_definition(self.fk_table_name)
        fk_table_column_name = fk_table_definition.find_reference_to_table(
            self.table_name
        ).get("column_name")
        update_data.update({
            fk_table_column_name: int(self.resource_id),
        })
        self.api_client.get_endpoint(self.fk_table_name).update(
            self.fk_resource_id,
            update_data
        )
        self.success_url = "%s?category=%s" % (
            reverse_lazy(self.success_reverse_base, kwargs={
                "resource_id": self.resource_id,
            }),
            self.category
        )
        fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(
            self.fk_resource_id
        )
        messages.success(
            self.request,
            f"Updated {humanise_resource_type(self.fk_table_name).title()} {fk_resource.pk}."
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        update_only_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=self.disabled_properties
        )
        kwargs.update({
            "fields": update_only_form_config.get_fields(),
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(
            self.fk_resource_id
        )
        context.update({
            "title": f"{resource_label(self.resource.as_dict(), self.resource_type, self.resource_id)} | Overview",
            "resource_name": resource_label(
                self.resource.as_dict(), self.resource_type, self.resource_id
            ),
            "main_heading": resource_label(
                fk_resource.as_dict(), self.fk_table_name, self.fk_resource_id
            ),
            "resource": self.resource.as_dict(),
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "table_name": self.fk_table_name,
            "fk_resource_id": self.fk_resource_id,
            "fk_resource_type": self.fk_table_name,
            "fk_table_name": self.fk_table_name,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "one_to_one_field_popup_section_reverse_base": self.one_to_one_field_popup_section_reverse_base,
            "one_to_many_field_popup_section_reverse_base": self.one_to_many_field_popup_section_reverse_base,
            "toc_list_items": self.get_toc_list_items(),
            "fk_table_toc_list_items": self.get_fk_table_toc_list_items(),
            "forms_by_category": self.get_forms_by_category(
                self.fk_table_form_config,
                initial=fk_resource.as_dict()
            ),
            "toast_template": render_to_string("editor/toast_template.html", {}),
            "text_array_field_list_item_template": render_to_string("editor/field_templates/text_array_field_list_item_template.html", {}),
        })
        return context


class NewOneToManyForeignKeyResourceEditorView(FormView):
    template_name = "editor/editor_for_foreign_key_fields/new_fk_editor.html"
    form_class = FormWithDynamicallyPopulatedFields
    success_reverse_base: str

    table_name: str
    column_metadata_table_name: str
    disabled_properties: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_table_name = self.kwargs["fk_table_name"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_properties"):
            self.disabled_properties = list()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_properties=self.disabled_properties
        )
        self.category = self.form_config.get_fields().get(
            self.fk_table_name
        ).category
        self.fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=self.disabled_properties
        )
        return super().dispatch(request, *args, **kwargs)

    def get_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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

    def form_valid(self, form):
        registration_data = form.cleaned_data
        fk_table_definition = self.openapi_spec.get_definition(self.fk_table_name)
        fk_table_column_name = fk_table_definition.find_reference_to_table(
            self.table_name
        ).get("column_name")
        registration_data.update({
            fk_table_column_name: int(self.resource_id),
        })
        new_resource = self.api_client.get_endpoint(self.fk_table_name).register(
            registration_data
        )
        self.success_url = "%s?category=%s" % (
            reverse_lazy(self.success_reverse_base, kwargs={
                "resource_id": self.resource_id,
            }),
            self.category
        )
        messages.success(
            self.request,
            f"Registered {humanise_resource_type(self.fk_table_name).title()} {new_resource.pk}."
        )
        return super().form_valid(form)

    def get_copy_source(self) -> dict:
        """The row being copied, when ?copy_from=<id> is given."""
        copy_from = self.request.GET.get("copy_from")
        if not copy_from:
            return {}
        endpoint = self.api_client.get_endpoint(self.fk_table_name)
        source = endpoint.get(copy_from)
        if source is None or source.as_dict() is None:
            raise Http404(f"No {self.fk_table_name} with id {copy_from} to copy")
        row = dict(source.as_dict())
        # Identity and parentage belong to the new row, not the copied one.
        for key in (endpoint.definition.pk_column_name, "created_at", "updated_at"):
            row.pop(key, None)
        return row

    def get_forms_by_category(
            self,
            form_config: FormConfig,
            initial: dict | None = None):
        forms_by_category = dict()
        for category in form_config.get_field_categories():
            relational = {
                name
                for name, metadata in self.fk_table_form_config.get_properties().items()
                if metadata.refers_to_table_name or metadata.created_from_table_name
            }
            fields = {
                name: field
                for name, field in form_config.get_fields_for_category(category).items()
                if name not in relational
            }
            form_for_category = FormWithDynamicallyPopulatedFields(
                fields=fields,
                initial=initial
            )
            if not category:
                forms_by_category.update({
                    UNKNOWN_ATTRIBUTE_CATEGORY: form_for_category,
                })
                continue
            forms_by_category.update({
                category: form_for_category,
            })
        return forms_by_category

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.get_copy_source())
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # NOTE: only handles the fields processed at form submission - the form fields
        # which are displayed in the wizard are handled in self.get_forms_by_category().
        # Everything the row has, so it can be filled in one pass rather than
        # created and then immediately edited. Foreign keys are excluded: they
        # render as relational sections, which need a row that does not exist
        # yet. Required fields are still marked, so what is needed stays clear.
        relational = {
            name
            for name, metadata in self.fk_table_form_config.get_properties().items()
            if metadata.refers_to_table_name or metadata.created_from_table_name
        }
        fields = {
            name: field
            for name, field in self.fk_table_form_config.get_fields().items()
            if name not in relational
        }
        kwargs.update({"fields": fields})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update({
            "title": f"{resource_label(self.resource.as_dict(), self.resource_type, self.resource_id)} | Overview",
            "resource_name": resource_label(
                self.resource.as_dict(), self.resource_type, self.resource_id
            ),
            "main_heading": f"New {humanise_resource_type(self.fk_table_name).title()}",
            "resource": self.resource.as_dict(),
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "table_name": self.fk_table_name,
            "fk_resource_type": self.fk_table_name,
            "fk_table_name": self.fk_table_name,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "toc_list_items": self.get_toc_list_items(),
            "fk_table_toc_list_items": self.get_fk_table_toc_list_items(),
            "forms_by_category": self.get_forms_by_category(
                self.fk_table_form_config,
                initial=self.get_initial()
            ),
        })
        return context


class OneToOneForeignKeyResourceEditorView(FormView):
    form_class = FormWithDynamicallyPopulatedFields
    template_name = "editor/editor_for_foreign_key_fields/fk_update_editor.html"
    success_reverse_base: str

    table_name: str
    column_metadata_table_name: str
    disabled_properties: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_column_name = self.kwargs["fk_column_name"]
        self.fk_resource_id = self.kwargs["fk_resource_id"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        definition = self.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_properties"):
            self.disabled_properties = list()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_properties=[
                TableNames.APPLICATION_MICROSERVICE,
                *self.disabled_properties,
            ]
        )
        self.category = self.form_config.get_fields().get(
            self.fk_column_name
        ).category
        self.fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=[
                TableNames.APPLICATION_MICROSERVICE,
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
            form_for_category = FormWithDynamicallyPopulatedFields(
                fields=form_config.get_fields_for_category(category),
                initial=initial
            )
            if not category:
                forms_by_category.update({
                    UNKNOWN_ATTRIBUTE_CATEGORY: form_for_category,
                })
                continue
            forms_by_category.update({
                category: form_for_category,
            })
        return forms_by_category

    def get_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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

    def form_valid(self, form):
        update_data = form.cleaned_data
        self.api_client.get_endpoint(self.fk_table_name).update(
            self.fk_resource_id,
            update_data
        )
        self.api_client.get_endpoint(self.table_name).update(
            self.resource_id,
            {
                self.fk_column_name: self.fk_resource_id,
            },
            set_updated_at_to_now=True
        )
        self.success_url = "%s?category=%s" % (
            reverse_lazy(self.success_reverse_base, kwargs={
                "resource_id": self.resource_id,
            }),
            self.category
        )
        fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(
            self.fk_resource_id
        )
        messages.success(
            self.request,
            f"Updated {humanise_resource_type(self.fk_table_name).title()} {fk_resource.pk}."
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        foreign_key_properties = [
            property_name
            for property_name, metadata in self.fk_table_form_config.get_properties().items()
            if (metadata.refers_to_table_name
                or metadata.created_from_table_name)
        ]
        update_only_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=[
                TableNames.APPLICATION_MICROSERVICE,
                *foreign_key_properties,
            ]
        )
        kwargs.update({
            "fields": update_only_form_config.get_fields(),
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(
            self.fk_resource_id
        )
        context.update({
            "title": f"{resource_label(self.resource.as_dict(), self.resource_type, self.resource_id)} | Overview",
            "resource_name": resource_label(
                self.resource.as_dict(), self.resource_type, self.resource_id
            ),
            "main_heading": resource_label(
                fk_resource.as_dict(), self.fk_table_name, self.fk_resource_id
            ),
            "resource": self.resource.as_dict(),
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "table_name": self.fk_table_name,
            "fk_resource_id": self.fk_resource_id,
            "fk_resource_type": self.fk_table_name,
            "fk_column_name": self.fk_column_name,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "one_to_one_field_popup_section_reverse_base": self.one_to_one_field_popup_section_reverse_base,
            "one_to_many_field_popup_section_reverse_base": self.one_to_many_field_popup_section_reverse_base,
            "toc_list_items": self.get_toc_list_items(),
            "fk_table_toc_list_items": self.get_fk_table_toc_list_items(),
            "forms_by_category": self.get_forms_by_category(
                self.fk_table_form_config,
                initial=fk_resource.as_dict()
            ),
            "toast_template": render_to_string("editor/toast_template.html", {}),
            "text_array_field_list_item_template": render_to_string("editor/field_templates/text_array_field_list_item_template.html", {}),
        })
        return context


class NewOneToOneForeignKeyResourceEditorView(FormView):
    template_name = "editor/editor_for_foreign_key_fields/new_fk_editor.html"
    form_class = FormWithDynamicallyPopulatedFields
    success_reverse_base: str

    table_name: str
    column_metadata_table_name: str
    disabled_properties: list[str]

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_column_name = self.kwargs["fk_column_name"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        definition = self.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        if not hasattr(self, "disabled_properties"):
            self.disabled_properties = list()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            disabled_properties=[
                TableNames.APPLICATION_MICROSERVICE,
                *self.disabled_properties,
            ]
        )
        self.category = self.form_config.get_fields().get(
            self.fk_column_name
        ).category
        self.fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=self.fk_table_name,
            disabled_properties=[
                TableNames.APPLICATION_MICROSERVICE,
                *self.disabled_properties,
            ]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_toc_list_items(self):
        category_names = list(set(
            resource.as_dict().get("category", "")
            for resource in self.column_metadata
            if (resource.as_dict().get("table_name", "") == self.column_metadata_table_name
                and resource.as_dict().get("column_name", "") not in self.disabled_properties)
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

    def form_valid(self, form):
        registration_data = form.cleaned_data
        new_resource = self.api_client.get_endpoint(self.fk_table_name).register(
            registration_data
        )
        self.api_client.get_endpoint(self.table_name).update(
            self.resource_id,
            {
                self.fk_column_name: new_resource.pk,
            },
            set_updated_at_to_now=True
        )
        self.success_url = "%s?category=%s" % (
            reverse_lazy(self.success_reverse_base, kwargs={
                "resource_id": self.resource_id,
            }),
            self.category
        )
        messages.success(
            self.request,
            f"Registered {humanise_resource_type(self.fk_table_name).title()} {new_resource.pk}."
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "fields": self.fk_table_form_config.get_required_fields(),
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update({
            "title": f"{resource_label(self.resource.as_dict(), self.resource_type, self.resource_id)} | Overview",
            "resource_name": resource_label(
                self.resource.as_dict(), self.resource_type, self.resource_id
            ),
            "main_heading": f"New {humanise_resource_type(self.fk_table_name).title()}",
            "resource": self.resource.as_dict(),
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "table_name": self.fk_table_name,
            "fk_resource_type": self.fk_table_name,
            "fk_table_name": self.fk_table_name,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "toc_list_items": self.get_toc_list_items(),
        })
        return context
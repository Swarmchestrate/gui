from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import FormView

from .forms import FormWithDynamicallyPopulatedFields
from .view_helpers import ForeignKeyEditorViewMixin
from postgrest.forms.form_config import FormConfig
from postgrest.table_names import TableNames
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_resource_type, resource_label


class ForeignKeyEditorView(ForeignKeyEditorViewMixin, FormView):
    def get_form_fields_for_category(
            self,
            form_config: FormConfig,
            category: str):
        fields = form_config.get_fields_for_category(category)
        return fields

    def get_forms_by_category(
            self,
            form_config: FormConfig,
            initial: dict | None = None):
        forms_by_category = dict()
        for category in form_config.get_field_categories():
            form_for_category = FormWithDynamicallyPopulatedFields(
                fields=self.get_form_fields_for_category(form_config, category),
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

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            "toc_list_items": self.get_toc_list_items(),
            "fk_table_toc_list_items": self.get_fk_table_toc_list_items(),
            "forms_by_category": self.get_forms_by_category(
                self.fk_table_form_config,
                initial=self.get_initial()
            ),
            "text_array_field_list_item_template": render_to_string("editor/field_templates/text_array_field_list_item_template.html", {}),
        })
        return kwargs


class OneToManyForeignKeyEditorView(ForeignKeyEditorView):
    form_class = FormWithDynamicallyPopulatedFields
    template_name = "editor/editor_for_foreign_key_fields/fk_update_editor.html"
    success_reverse_base: str

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_table_name = self.kwargs["fk_table_name"]
        self.fk_resource_id = self.kwargs["fk_resource_id"]
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        self.fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(self.fk_resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        if self.fk_resource is None or self.fk_resource.as_dict() is None:
            raise Http404(f"No {self.fk_table_name} with id {self.fk_resource_id}")
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = self.get_form_config()
        self.category = self.form_config.get_fields().get(
            self.fk_table_name
        ).category
        self.fk_table_form_config = self.get_fk_table_form_config()
        return super().dispatch(request, *args, **kwargs)

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
        messages.success(
            self.request,
            f"Updated {humanise_resource_type(self.fk_table_name).title()} {self.fk_resource.pk}."
        )
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.fk_resource.as_dict())
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        update_only_form_config = self.get_fk_table_form_config()
        kwargs.update({
            "fields": update_only_form_config.get_fields(),
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
            "main_heading": resource_label(
                self.fk_resource.as_dict(), self.fk_table_name, self.fk_resource_id
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
            "toast_template": render_to_string("editor/toast_template.html", {}),
        })
        return context


class NewOneToManyForeignKeyEditorView(ForeignKeyEditorView):
    template_name = "editor/editor_for_foreign_key_fields/new_fk_editor.html"
    form_class = FormWithDynamicallyPopulatedFields
    success_reverse_base: str

    editor_reverse_base: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_table_name = self.kwargs["fk_table_name"]
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = self.get_form_config()
        self.category = self.form_config.get_fields().get(
            self.fk_table_name
        ).category
        self.fk_table_form_config = self.get_fk_table_form_config()
        return super().dispatch(request, *args, **kwargs)

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

    def get_form_fields_for_category(self, form_config, category):
        unprocessed_fields = super().get_form_fields_for_category(form_config, category)
        # Remove relational fields as these require an ID to a resource that doesn't
        # exist yet.
        relational = {
            name
            for name, metadata in self.fk_table_form_config.get_properties().items()
            if metadata.refers_to_table_name or metadata.created_from_table_name
        }
        fields = {
            name: field
            for name, field in unprocessed_fields.items()
            if name not in relational
        }
        return fields

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
        self.disabled_relational_fields = {
            metadata.title
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
            "disabled_relational_fields": self.disabled_relational_fields,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
        })
        return context


class OneToOneForeignKeyEditorView(ForeignKeyEditorView):
    form_class = FormWithDynamicallyPopulatedFields
    template_name = "editor/editor_for_foreign_key_fields/fk_update_editor.html"
    success_reverse_base: str

    editor_reverse_base: str
    resource_type: str

    def get_fk_table_form_config_kwargs(self):
        kwargs = super().get_fk_table_form_config_kwargs()
        kwargs.update({
            "disabled_properties": [TableNames.APPLICATION_MICROSERVICE],
        })
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_column_name = self.kwargs["fk_column_name"]
        self.fk_resource_id = self.kwargs["fk_resource_id"]
        definition = self.openapi_spec.get_definition(self.table_name)
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        self.fk_resource = self.api_client.get_endpoint(self.fk_table_name).get(self.fk_resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        if self.fk_resource is None or self.fk_resource.as_dict() is None:
            raise Http404(f"No {self.fk_table_name} with id {self.fk_resource_id}")
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = self.get_form_config()
        self.category = self.form_config.get_fields().get(
            self.fk_column_name
        ).category
        self.fk_table_form_config = self.get_fk_table_form_config()
        return super().dispatch(request, *args, **kwargs)

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
        messages.success(
            self.request,
            f"Updated {humanise_resource_type(self.fk_table_name).title()} {self.fk_resource.pk}."
        )
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.fk_resource.as_dict())
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Since FKs are updated separately to this resource, there's no point
        # in passing any update data for them. It's update only as the FK properties
        # still need to be present when rendering the form.
        foreign_key_properties = [
            property_name
            for property_name, metadata in self.fk_table_form_config.get_properties().items()
            if (metadata.refers_to_table_name
                or metadata.created_from_table_name)
        ]
        update_only_form_config = self.get_fk_table_form_config(
            extra_form_config_kwargs={
                "disabled_properties": [
                    *self.get_fk_table_form_config_kwargs().get(
                        "disabled_properties"
                    , []),
                    *foreign_key_properties,
                ]
            }
        )
        kwargs.update({
            "fields": update_only_form_config.get_fields(),
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
            "main_heading": resource_label(
                self.fk_resource.as_dict(), self.fk_table_name, self.fk_resource_id
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
            "toast_template": render_to_string("editor/toast_template.html", {}),
        })
        return context


class NewOneToOneForeignKeyEditorView(ForeignKeyEditorView):
    template_name = "editor/editor_for_foreign_key_fields/new_fk_editor.html"
    form_class = FormWithDynamicallyPopulatedFields
    success_reverse_base: str

    editor_reverse_base: str
    resource_type: str

    def get_fk_table_form_config_kwargs(self):
        kwargs = super().get_fk_table_form_config_kwargs()
        kwargs.update({
            "disabled_properties": [TableNames.APPLICATION_MICROSERVICE],
        })
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.fk_column_name = self.kwargs["fk_column_name"]
        definition = self.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        self.resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        if self.resource is None or self.resource.as_dict() is None:
            raise Http404(f"No {self.table_name} with id {self.resource_id}")
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        self.form_config = self.get_form_config()
        self.category = self.form_config.get_fields().get(
            self.fk_column_name
        ).category
        self.fk_table_form_config = self.get_fk_table_form_config()
        return super().dispatch(request, *args, **kwargs)

    def get_form_fields_for_category(self, form_config, category):
        unprocessed_fields = super().get_form_fields_for_category(form_config, category)
        # Remove relational fields as these require an ID to a resource that doesn't
        # exist yet.
        relational = {
            name
            for name, metadata in self.fk_table_form_config.get_properties().items()
            if metadata.refers_to_table_name or metadata.created_from_table_name
        }
        self.disabled_relational_fields = {
            metadata.title
            for name, metadata in self.fk_table_form_config.get_properties().items()
            if metadata.refers_to_table_name or metadata.created_from_table_name
        }
        fields = {
            name: field
            for name, field in unprocessed_fields.items()
            if name not in relational
        }
        return fields

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
            "disabled_relational_fields": self.disabled_relational_fields,
            "initial_category": self.category,
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
        })
        return context
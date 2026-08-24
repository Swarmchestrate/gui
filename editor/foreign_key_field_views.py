import logging
from http import HTTPStatus

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View

from editor.forms import ForeignKeyFormWithDynamicallyPopulatedFields
from editor.view_helpers import get_form_config_for_table
from postgrest.api import ApiClient, Resource
from postgrest.table_names import TableNames
from resource_management.forms import ResourceDeletionForm
from utils.helpers import generate_random_string
from utils.humanise import humanise_resource_type, resource_label


logger = logging.getLogger(__name__)


class OneToOneFieldPopupSectionView(View):
    table_name: str

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "table_name"):
            self.table_name = kwargs["table_name"]
        self.resource_id = int(kwargs["resource_id"])
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
            # Some choices depend on the row this one hangs off.
            choices_context={"parent_table": self.table_name, "parent_id": self.resource_id},
            disabled_properties=[TableNames.APPLICATION_MICROSERVICE]
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
        return render_to_string("editor/foreign_key_fields/popup_based/one_to_one_field_popup_section.html", {
            "field_name": self.fk_column_name,
            "resource": self.get_fk_resource(),
            "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                fields=self.form_config.get_fields(),
                initial=initial
            ),
            "resource_type": self.fk_table_name,
        })

    def get_new_dialog_template(self):
        return render_to_string(
            "editor/dialogs/new_dialog.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_prefix=f'new_{self.fk_column_name}'
                ),
                "form_id": f"new-form-{generate_random_string()}",
                "new_resource_url": reverse_lazy(
                    "postgrest:new_one_to_one_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"new-{self.fk_column_name}-dialog",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get_update_dialog_template(self, fk_resource: Resource):
        fk_resource_id = None
        initial = dict()
        if fk_resource:
            fk_resource_id = fk_resource.pk
            initial = fk_resource.as_dict()
        return render_to_string(
            "editor/dialogs/update_dialog.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_suffix=f"{self.fk_column_name}",
                    initial=initial
                ),
                "form_id": f"update-form-{generate_random_string()}",
                "update_resource_url": reverse_lazy(
                    "postgrest:update_one_to_one_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"update-{self.fk_column_name}-dialog",
                "resource_id": fk_resource_id,
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get_delete_dialog_template(self, fk_resource: Resource):
        fk_resource_id = None
        initial = dict()
        if fk_resource:
            fk_resource_id = fk_resource.pk
            initial = {"resource_id_to_delete": fk_resource_id}
        return render_to_string(
            "editor/dialogs/delete_dialog.html",
            {
                "form": ResourceDeletionForm(
                    initial=initial
                ),
                "form_id": f"delete-form-{generate_random_string()}",
                "delete_resource_url": reverse_lazy(
                    "postgrest:delete_one_to_one_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"delete-{self.fk_column_name}-dialog",
                "resource_id": fk_resource_id,
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        fk_resource = self.get_fk_resource()
        return JsonResponse({
            "section": self.get_section_template(fk_resource),
            "update_dialog": self.get_update_dialog_template(fk_resource),
            "delete_dialog": self.get_delete_dialog_template(fk_resource),
            "new_dialog": self.get_new_dialog_template(),
        })


class OneToManyFieldPopupSectionView(View):
    table_name: str
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "table_name"):
            self.table_name = self.kwargs["table_name"]
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_table_name = self.kwargs["fk_table_name"]
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
            # Some choices depend on the row this one hangs off.
            choices_context={"parent_table": self.table_name, "parent_id": self.resource_id},
            disabled_properties=[f"{TableNames.APPLICATION_MICROSERVICE}_id"]
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
        return render_to_string("editor/foreign_key_fields/popup_based/one_to_many_field_popup_section.html", {
            "field_name": self.fk_table_name,
            "forms_for_existing_resources": forms_for_existing_fk_resources,
            "resource_type": self.fk_table_name,
        })

    def get_list_item_template(self):
        return render_to_string(
            "editor/foreign_key_fields/popup_based/one_to_many_field_popup_list_item.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_suffix="__resource_id__",
                ),
                "resource_id": "__resource_id__",
                "resource_type": self.fk_table_name,
                "field": {"name": self.fk_table_name},
                "field_name": self.fk_table_name,
                # Use humanise_resource_type() instead of resource_label() as
                # the resource may not exist yet.
                "label": f"{humanise_resource_type(self.fk_table_name).title()} __resource_id__",
            },
            request=self.request
        )

    def get_new_dialog_template(self):
        return render_to_string(
            "editor/dialogs/new_dialog.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_prefix=f'new_{self.fk_table_name}'
                ),
                "form_id": f"new-form-{generate_random_string()}",
                "new_resource_url": reverse_lazy(
                    "postgrest:new_one_to_many_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_table_name": self.fk_table_name,
                    }
                ),
                "dialog_id": f"new-{self.fk_table_name}-dialog",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get_update_form(self, fk_resource_id: int | str, initial: dict):
        return ForeignKeyFormWithDynamicallyPopulatedFields(
            fields=self.form_config.get_fields(),
            id_suffix=f"{self.fk_table_name}_{fk_resource_id}",
            initial=initial,
        )

    def get_update_dialog_template(self, fk_resource: Resource = None):
        fk_resource_id = "__resource_id__"
        initial = dict()
        if fk_resource:
            fk_resource_id = fk_resource.pk
            initial = fk_resource.as_dict()
        return render_to_string(
            "editor/dialogs/update_dialog.html",
            {
                "form": self.get_update_form(
                    fk_resource_id,
                    initial
                ),
                "form_id": f"update-form-{generate_random_string()}",
                "resource_id": fk_resource_id,
                "update_resource_url": reverse_lazy(
                    "postgrest:update_one_to_many_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_table_name": self.fk_table_name,
                        "fk_resource_id": fk_resource_id,
                    },
                ),
                "dialog_id": f"update-{self.fk_table_name}-{fk_resource_id}-dialog",
                "dialog_extra_classes": "col-lg-10",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )
    
    def get_delete_form(self, fk_resource_id: str | int):
        return ResourceDeletionForm(
            initial={
                "resource_id_to_delete": fk_resource_id
            }
        )

    def get_delete_dialog_template(self, fk_resource: Resource = None):
        fk_resource_id = "__resource_id__"
        if fk_resource:
            fk_resource_id = fk_resource.pk
        return render_to_string(
            "editor/dialogs/delete_dialog.html",
            {
                "form": self.get_delete_form(fk_resource_id),
                "form_id": f"delete-form-{generate_random_string()}",
                "resource_id": fk_resource_id,
                "delete_resource_url": reverse_lazy(
                    "postgrest:delete_one_to_many_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_table_name": self.fk_table_name,
                        "fk_resource_id": fk_resource_id,
                    },
                ),
                "dialog_id": f"delete-{self.fk_table_name}-{fk_resource_id}-dialog",
                "dialog_extra_classes": "col-lg-10",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        fk_resources = self.get_resources()
        return JsonResponse({
            "section": self.get_section_template({
                fk_resource.pk: {
                    "update_form": self.get_update_form(
                        fk_resource.pk,
                        fk_resource.as_dict()
                    ),
                    "delete_form": self.get_delete_form(fk_resource.pk),
                    "label": resource_label(
                        fk_resource.as_dict(), self.fk_table_name, fk_resource.pk
                    ),
                }
                for fk_resource in fk_resources
            }),
            "new_dialog": self.get_new_dialog_template(),
            "resource_dialogs": {
                fk_resource.pk: {
                    "update_dialog": self.get_update_dialog_template(
                        fk_resource
                    ),
                    "delete_dialog": self.get_delete_dialog_template(
                        fk_resource
                    ),
                }
                for fk_resource in fk_resources
            },
            "templates": {
                "update_dialog": render_to_string(
                    "editor/utils/to_json_script.html",
                    {
                        "content": self.get_update_dialog_template(),
                        "content_id": f"{self.fk_table_name}-update_dialog-form-template",
                    },
                    request=self.request
                ),
                "delete_dialog": render_to_string(
                    "editor/utils/to_json_script.html",
                    {
                        "content": self.get_delete_dialog_template(),
                        "content_id": f"{self.fk_table_name}-delete_dialog-form-template",
                    },
                    request=self.request
                ),
                "list_item": render_to_string(
                    "editor/utils/to_json_script.html",
                    {
                        "content": self.get_list_item_template(),
                        "content_id": f"{self.fk_table_name}-list_item-form-template",
                    },
                    request=self.request
                ),
            },
            "add_url": reverse_lazy(
                "postgrest:new_one_to_many_relation",
                kwargs={
                    "table_name": self.table_name,
                    "resource_id": self.resource_id,
                    "fk_table_name": self.fk_table_name,
                }
            ),
        })


class OneToOneFieldSectionView(View):
    table_name: str
    
    new_foreign_key_editor_reverse_base: str
    foreign_key_update_editor_reverse_base: str

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "table_name"):
            self.table_name = kwargs["table_name"]
        self.resource_id = int(kwargs["resource_id"])
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
            # Some choices depend on the row this one hangs off.
            choices_context={"parent_table": self.table_name, "parent_id": self.resource_id},
            disabled_properties=[TableNames.APPLICATION_MICROSERVICE]
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
        fk_resource_id = None
        if fk_resource:
            initial = fk_resource.as_dict()
            fk_resource_id = fk_resource.pk
        return render_to_string("editor/foreign_key_fields/one_to_one_field_section.html", {
            "field_name": self.fk_column_name,
            "resource_id": self.resource_id,
            "resource": fk_resource,
            "fk_resource_id": fk_resource_id,
            "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                fields=self.form_config.get_fields(),
                initial=initial
            ),
            "resource_type": self.fk_table_name,
            "new_foreign_key_editor_reverse_base": self.new_foreign_key_editor_reverse_base,
            "foreign_key_update_editor_reverse_base": self.foreign_key_update_editor_reverse_base,
        })

    def get_delete_dialog_template(self, fk_resource: Resource):
        fk_resource_id = None
        initial = dict()
        if fk_resource:
            fk_resource_id = fk_resource.pk
            initial = {"resource_id_to_delete": fk_resource_id}
        return render_to_string(
            "editor/dialogs/delete_dialog.html",
            {
                "form": ResourceDeletionForm(
                    initial=initial
                ),
                "form_id": f"delete-form-{generate_random_string()}",
                "delete_resource_url": reverse_lazy(
                    "postgrest:delete_one_to_one_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"delete-{self.fk_column_name}-dialog",
                "resource_id": fk_resource_id,
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        fk_resource = self.get_fk_resource()
        return JsonResponse({
            "section": self.get_section_template(fk_resource),
            "delete_dialog": self.get_delete_dialog_template(fk_resource),
        })


class OneToManyFieldSectionView(View):
    table_name: str
    resource_type: str
    
    new_foreign_key_editor_reverse_base: str
    foreign_key_update_editor_reverse_base: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_table_name = self.kwargs["fk_table_name"]
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
            # Some choices depend on the row this one hangs off.
            choices_context={"parent_table": self.table_name, "parent_id": self.resource_id},
            disabled_properties=[f"{TableNames.APPLICATION_MICROSERVICE}_id"]
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
        return render_to_string("editor/foreign_key_fields/one_to_many_field_section.html", {
            "resource_id": self.resource_id,
            "field_name": self.fk_table_name,
            "forms_for_existing_resources": forms_for_existing_fk_resources,
            "resource_type": self.fk_table_name,
            "new_foreign_key_editor_reverse_base": self.new_foreign_key_editor_reverse_base,
            "foreign_key_update_editor_reverse_base": self.foreign_key_update_editor_reverse_base,
        })
    
    def get_delete_form(self, fk_resource_id: str | int):
        return ResourceDeletionForm(
            initial={
                "resource_id_to_delete": fk_resource_id
            }
        )

    def get_delete_dialog_template(self, fk_resource: Resource = None):
        fk_resource_id = "__resource_id__"
        if fk_resource:
            fk_resource_id = fk_resource.pk
        return render_to_string(
            "editor/dialogs/delete_dialog.html",
            {
                "form": self.get_delete_form(fk_resource_id),
                "form_id": f"delete-form-{generate_random_string()}",
                "resource_id": fk_resource_id,
                "delete_resource_url": reverse_lazy(
                    "postgrest:delete_one_to_many_relation",
                    kwargs={
                        "table_name": self.table_name,
                        "resource_id": self.resource_id,
                        "fk_table_name": self.fk_table_name,
                        "fk_resource_id": fk_resource_id,
                    },
                ),
                "dialog_id": f"delete-{self.fk_table_name}-{fk_resource_id}-dialog",
                "dialog_extra_classes": "col-lg-10",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        fk_resources = self.get_resources()
        return JsonResponse({
            "section": self.get_section_template({
                fk_resource.pk: {
                    "delete_form": self.get_delete_form(fk_resource.pk),
                    "label": resource_label(
                        fk_resource.as_dict(), self.fk_table_name, fk_resource.pk
                    ),
                }
                for fk_resource in fk_resources
            }),
            "resource_dialogs": {
                fk_resource.pk: {
                    "delete_dialog": self.get_delete_dialog_template(
                        fk_resource
                    ),
                }
                for fk_resource in fk_resources
            },
            "add_url": reverse_lazy(
                self.new_foreign_key_editor_reverse_base,
                kwargs={
                    "resource_id": self.resource_id,
                    "fk_table_name": self.fk_table_name,
                }
            ),
        })


class OneToOneFieldOverviewSubsectionView(TemplateView):
    template_name = "editor/overview/foreign_key_fields/one_to_one_field_overview_subsection.html"

    def get(self, request, *args, **kwargs):
        fk_column_name = kwargs["fk_column_name"]
        fk_resource_id = kwargs["fk_resource_id"]
        # Get resource referred to by main resource.
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        definition = api_client.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(fk_column_name)
        fk_table_endpoint = api_client.get_endpoint(self.fk_table_name)
        self.fk_resource = fk_table_endpoint.get(fk_resource_id)
        # Get the titles for the FK table column names so the properties (and their values)
        # can be listed out in a more readable way in the overview page.
        column_metadata = api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "column_metadata_table_name"):
            self.column_metadata_table_name = self.table_name
        fk_table_form_config = get_form_config_for_table(
            self.fk_table_name,
            api_client.openapi_spec,
            column_metadata,
            column_metadata_table_name=self.column_metadata_table_name,
            infer_one_to_many_properties=False
        )
        self.properties_as_dict = fk_table_form_config.get_properties()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            "fk_table_name": self.fk_table_name,
            "fk_resource": self.fk_resource,
            "overview_data": {
                property_name: {
                    "title": metadata.title,
                    "value": self.fk_resource.as_dict().get(property_name),
                    # Pass the rest of the property metadata for further configuration
                    # in the overview HTML template.
                    "additional_metadata": metadata,
                }
                for property_name, metadata in self.properties_as_dict.items()
            }
        })
        return kwargs


class OneToManyFieldOverviewSubsectionView(TemplateView):
    template_name = "editor/overview/foreign_key_fields/one_to_many_field_overview_subsection.html"

    def get(self, request, *args, **kwargs):
        resource_id = kwargs["resource_id"]
        self.fk_table_name = kwargs["fk_table_name"]
        # Get resources referring to the main resources.
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        referring_tables = api_client.openapi_spec.find_references_to_table(
            self.table_name
        )
        fk_table_column_name = referring_tables.get(self.fk_table_name)
        fk_table_endpoint = api_client.get_endpoint(self.fk_table_name)
        self.fk_resources = fk_table_endpoint.get_resources_referencing_resource_id(
            fk_table_column_name,
            resource_id
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            "fk_table_name": self.fk_table_name,
            "fk_resources": self.fk_resources,
        })
        return kwargs
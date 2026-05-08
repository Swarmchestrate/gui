import logging
from http import HTTPStatus

from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from editor.forms import ForeignKeyFormWithDynamicallyPopulatedFields
from editor.view_helpers import get_form_config_for_table
from postgrest.new_api import ApiClient, Resource
from resource_management.forms import ResourceDeletionForm


logger = logging.getLogger(__name__)


# Views for managing one-to-one relations between tables.
# E.g., A cloud capacity (locality_id) -> locality.
class NewOneToOneRelationFormView(FormView):
    table_name: str
    fk_table_name: str
    form_class = ForeignKeyFormWithDynamicallyPopulatedFields

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_column_name = self.kwargs["fk_column_name"]
        # API client is instantiated here so it doesn't
        # fetch the OpenAPI spec twice.
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        definition = self.api_client.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        if not self.fk_table_name:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fk_resource_endpoint = self.api_client.get_endpoint(self.fk_table_name)
        # Create the new resource in the foreign key table
        new_fk_resource = fk_resource_endpoint.register(form.cleaned_data)
        # Assign the new resource's ID to corresponding property
        self.api_client.get_endpoint(self.table_name).update(
            self.resource_id,
            {
                self.fk_column_name: new_fk_resource.pk
            },
        )
        message = f"Added new {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        resource_data_for_response = new_fk_resource.as_dict()
        # The property name for PKs changes between resource
        # types, so add a "pk" property to make it easier for
        # the UI to work with.
        resource_data_for_response.update({
            "pk": new_fk_resource.pk,
        })
        return JsonResponse({"resource": resource_data_for_response})

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata_endpoint.get_resources(),
            infer_one_to_many_properties=False
        )
        kwargs.update({
            "fields": form_config.get_fields(),
        })
        return kwargs


class UpdateOneToOneRelationFormView(FormView):
    form_class = ForeignKeyFormWithDynamicallyPopulatedFields
    
    table_name: str
    resource: Resource

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_column_name = self.kwargs["fk_column_name"]
        # API client is instantiated here so it doesn't
        # fetch the OpenAPI spec twice.
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        definition = self.api_client.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        if not self.fk_table_name:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        fk_resource_id = int(resource.as_dict().get(self.fk_column_name))
        self.api_client.get_endpoint(self.fk_table_name).update(fk_resource_id, form.cleaned_data)
        message = f"Updated {self.fk_table_name} registration."
        resource = self.api_client.get_endpoint(self.fk_table_name).get(fk_resource_id)
        resource.as_dict().update(
            {"pk": resource.pk}
        )
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource.as_dict()})

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata_endpoint.get_resources(),
            infer_one_to_many_properties=False
        )
        kwargs.update({
            "fields": form_config.get_fields(),
        })
        return kwargs


class DeleteOneToOneRelationFormView(FormView):
    table_name: str
    form_class = ResourceDeletionForm

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_column_name = self.kwargs["fk_column_name"]
        # API client is instantiated here so it doesn't
        # fetch the OpenAPI spec twice.
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        definition = self.api_client.openapi_spec.get_definition(self.table_name)
        self.fk_table_name = definition.get_foreign_key_table_name_for_column(self.fk_column_name)
        if not self.fk_table_name:
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})

    def form_valid(self, form):
        resource = self.api_client.get_endpoint(self.table_name).get(self.resource_id)
        fk_resource_id = int(resource.as_dict().get(self.fk_column_name))
        self.api_client.get_endpoint(self.fk_table_name).delete(fk_resource_id)
        self.api_client.get_endpoint(self.table_name).update(
            self.resource_id,
            {
                self.fk_column_name: None
            }
        )
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"result": "success"})


# Views for managing one-to-many relations between tables.
# E.g., A cloud capacity -> capacity instance types (e.g.,
# referencing a capacity by a "capacity_id" column).

class NewOneToManyRelationFormView(FormView):
    form_class = ForeignKeyFormWithDynamicallyPopulatedFields
    table_name: str
    possible_fk_table_column_name: str

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
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        cleaned_data.update({self.fk_table_column_name: self.resource_id})
        new_fk_resource = self.api_client.get_endpoint(
            self.fk_table_name
        ).register(cleaned_data)
        resource_data_for_response = new_fk_resource.as_dict()
        # The property name for PKs changes between resource
        # types, so add a "pk" property to make it easier for
        # the UI to work with.
        resource_data_for_response.update({
            "pk": new_fk_resource.pk,
        })
        message = f"Added new {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource_data_for_response})

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata_endpoint.get_resources(),
            infer_one_to_many_properties=False
        )
        kwargs.update({
            "fields": form_config.get_fields(),
        })
        return kwargs


class UpdateOneToManyRelationFormView(FormView):
    form_class = ForeignKeyFormWithDynamicallyPopulatedFields
    table_name: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_resource_id = int(self.kwargs["fk_resource_id"])
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
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fk_resource = self.api_client.get_endpoint(
            self.fk_table_name
        ).get(self.fk_resource_id)
        # If FK resource is referencing another resource (e.g., a
        # capacity instance type is referencing another capacity)
        # don't proceed with the update.
        if not (fk_resource.as_dict().get(self.fk_table_column_name) == self.resource_id):
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        update_data = form.cleaned_data
        update_data.pop(self.fk_table_column_name)
        self.api_client.get_endpoint(
            self.fk_table_name
        ).update(self.fk_resource_id, update_data)
        message = f"Updated {self.fk_table_name} registration."
        fk_resource = self.api_client.get_endpoint(
            self.fk_table_name
        ).get(self.fk_resource_id)
        resource_data_for_response = fk_resource.as_dict()
        # The property name for PKs changes between resource
        # types, so add a "pk" property to make it easier for
        # the UI to work with.
        resource_data_for_response.update({
            "pk": fk_resource.pk,
        })
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"resource": resource_data_for_response})

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        column_metadata_endpoint = self.api_client.get_endpoint("column_metadata")
        form_config = get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            column_metadata_endpoint.get_resources(),
            infer_one_to_many_properties=False
        )
        kwargs.update({
            "fields": form_config.get_fields(),
        })
        return kwargs


class DeleteOneToManyRelationFormView(FormView):
    form_class = ResourceDeletionForm
    table_name: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = int(self.kwargs["resource_id"])
        self.fk_resource_id = int(self.kwargs["fk_resource_id"])
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
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fk_resource = self.api_client.get_endpoint(
            self.fk_table_name
        ).get(self.fk_resource_id)
        # If FK resource is referencing another resource (e.g., a
        # capacity instance type is referencing another capacity)
        # don't proceed with deletion.
        if not (fk_resource.as_dict().get(self.fk_table_column_name) == self.resource_id):
            return JsonResponse({}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
        self.api_client.get_endpoint(
            self.fk_table_name
        ).delete(self.fk_resource_id)
        message = f"Deleted {self.fk_table_name} registration."
        if self.request.accepts("text/html"):
            messages.success(self.request, message)
            return super().form_valid(form)
        return JsonResponse({"result": "success"})

    def form_invalid(self, form):
        logger.exception("form.errors", form.errors)
        if self.request.accepts("text/html"):
            messages.error(self.request, "The form submitted was not valid.")
            return super().form_invalid(form)
        return JsonResponse({"feedback": form.errors})


class OneToOneFieldEditorSectionView(View):
    table_name: str

    new_one_to_one_relation_reverse_base: str
    update_one_to_one_relation_reverse_base: str
    delete_one_to_one_relation_reverse_base: str

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
            infer_one_to_many_properties=False
        )
        return super().dispatch(request, *args, **kwargs)

    def get_resource(self):
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
    
    def get_section_template(self, resource: Resource):
        initial = dict()
        if resource:
            initial = resource.as_dict()
        return render_to_string("editor/foreign_key_fields/one_to_one_field_section.html", {
            "field_name": self.fk_column_name,
            "resource": self.get_resource(),
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
                "new_resource_url": reverse_lazy(
                    self.new_one_to_one_relation_reverse_base,
                    kwargs={
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"new-{self.fk_column_name}-dialog",
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get_update_dialog_template(self, resource: Resource):
        resource_id = None
        initial = dict()
        if resource:
            resource_id = resource.pk
            initial = resource.as_dict()
        return render_to_string(
            "editor/dialogs/update_dialog.html",
            {
                "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    fields=self.form_config.get_fields(),
                    id_suffix=f"{self.fk_column_name}",
                    initial=initial
                ),
                "update_resource_url": reverse_lazy(
                    self.update_one_to_one_relation_reverse_base,
                    kwargs={
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"update-{self.fk_column_name}-dialog",
                "resource_id": resource_id,
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get_delete_dialog_template(self, resource: Resource):
        resource_id = None
        initial = dict()
        if resource:
            resource_id = resource.pk
            initial = {"resource_id_to_delete": resource_id}
        return render_to_string(
            "editor/dialogs/delete_dialog.html",
            {
                "form": ResourceDeletionForm(
                    initial=initial
                ),
                "delete_resource_url": reverse_lazy(
                    self.delete_one_to_one_relation_reverse_base,
                    kwargs={
                        "resource_id": self.resource_id,
                        "fk_column_name": self.fk_column_name,
                    }
                ),
                "dialog_id": f"delete-{self.fk_column_name}-dialog",
                "resource_id": resource_id,
                "resource_type": self.fk_table_name,
            },
            request=self.request
        )

    def get(self, request, *args, **kwargs):
        resource = self.get_resource()
        return JsonResponse({
            "section": self.get_section_template(resource),
            "update_dialog": self.get_update_dialog_template(resource),
            "delete_dialog": self.get_delete_dialog_template(resource),
            "new_dialog": self.get_new_dialog_template(),
        })
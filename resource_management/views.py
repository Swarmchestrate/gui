import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import FormView, TemplateView, View
from django.views.generic.base import ContextMixin

from .exceptions import NameMissingException, SatBuilderException
from .forms import (
    CategoryOrderForm,
    ColumnMetadataDeletionForm,
    FieldOrderForm,
    MultiResourceDeletionForm,
    ResourceDeletionForm,
)
from .view_helpers import (
    DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT,
    get_composite_pk,
    get_ordered_fields_and_categories_for_table_name,
    get_postgrest_table_names,
    get_update_data_for_new_field_order,
)

from editor.forms import FormWithDynamicallyPopulatedFields
from editor.view_helpers import get_form_config_for_table
from postgrest.table_names import TableNames
from utils.humanise import (
    humanise_resource_type,
    humanise_resource_type_plural,
)
from postgrest.api import ApiClient, Resource


logger = logging.getLogger(__name__)


# Create your views here.
class ResourceListContextMixin(ContextMixin):
    resource_list_reverse: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"resource_list_reverse": self.resource_list_reverse})
        return context


class ResourceListFormView(TemplateView):
    template_name = "resource_management/resource_list.html"
    resource_deletion_form_class = ResourceDeletionForm
    multi_resource_deletion_form_class = MultiResourceDeletionForm

    table_name: str
    resource_type: str

    resource_list_reverse: str
    new_resource_reverse: str
    resource_deletion_reverse: str
    multi_resource_deletion_reverse: str
    editor_reverse_base: str
    editor_overview_reverse_base: str
    tosca_template_download_reverse_base: str

    def get_resource_list(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        return api_client.get_endpoint(self.table_name).get_resources()

    def dispatch(self, request, *args, **kwargs):
        self.resource_list = self.get_resource_list()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update({
            "title": humanise_resource_type_plural(self.resource_type).title(),
            "new_resource_reverse": self.new_resource_reverse,
            "resource_deletion_reverse": self.resource_deletion_reverse,
            "resource_deletion_forms": {
                resource.pk: self.resource_deletion_form_class(
                    id_suffix=str(i),
                    initial={
                        "resource_id_to_delete": resource.pk
                    },
                )
                for i, resource in enumerate(self.resource_list)
            },
            "multi_resource_deletion_reverse": self.multi_resource_deletion_reverse,
            "multi_resource_deletion_form": self.multi_resource_deletion_form_class(
                resource_ids=[
                    resource.pk for resource in self.resource_list
                ]
            ),
            "resources": {
                resource.pk: resource
                for resource in self.resource_list
            },
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "tosca_template_download_reverse_base": self.tosca_template_download_reverse_base,
            "resource_type": self.resource_type,
        })
        return context


class ResourceDeletionFormView(FormView):
    form_class = ResourceDeletionForm

    table_name: str
    resource_type: str

    resource_list_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(self.resource_list_reverse)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        resource_id_to_delete = form.cleaned_data.get("resource_id_to_delete")
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        api_client.get_endpoint(self.table_name).delete(resource_id_to_delete)
        success_msg = f"Deleted {humanise_resource_type(self.resource_type)} {resource_id_to_delete}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class MultiResourceDeletionFormView(FormView):
    form_class = MultiResourceDeletionForm

    api_client: ApiClient
    table_name: str
    resource_type: str

    resource_list_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.resource_list = self.api_client.get_endpoint(self.table_name).get_resources()
        self.success_url = reverse_lazy(self.resource_list_reverse)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "resource_ids": [
                resource.pk
                for resource in self.resource_list
            ]
        })
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type_plural(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        resource_ids_to_delete = [
            int(resource_id)
            for resource_id in form.cleaned_data.get("resource_ids_to_delete", [])
        ]
        self.api_client.get_endpoint(self.table_name).delete_many(resource_ids_to_delete)
        success_msg = f"Deleted 1 {humanise_resource_type(self.resource_type)}."
        if len(resource_ids_to_delete) != 1:
            success_msg = f"Deleted {len(resource_ids_to_delete)} {humanise_resource_type_plural(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class ToscaTemplateDownloadView(View):
    resource_id: int
    table_name: str
    resource_type: str
    resource_list_reverse: str
    
    def generate_sat_yaml(self) -> str:
        # Overridden in view subclasses
        pass

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = kwargs["resource_id"]
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            sat_yaml = self.generate_sat_yaml()
            response = HttpResponse(
                sat_yaml,
                content_type="application/yaml"
            )
            response["Content-Disposition"] = f"inline; filename={self.resource_type}_{self.resource_id}.yaml"
        except (NameMissingException, SatBuilderException, ValueError) as err:
            # These carry a message naming what the wizard still needs.
            logger.exception(str(err))
            messages.error(request, str(err))
            return redirect(self.resource_list_reverse)
        except Exception:
            error_msg = "Encountered an error whilst generating the SAT."
            logger.exception(error_msg)
            messages.error(request, error_msg)
            return redirect(self.resource_list_reverse)
        return response


# Column metadata management
class ColumnMetadataManagementListView(TemplateView):
    template_name = "resource_management/column_metadata_management_index.html"
    table_name = TableNames.COLUMN_METADATA

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Wizard Customisation",
            "table_names": get_postgrest_table_names(self.openapi_spec),
        })
        return context


class ColumnMetadataManagementForTableView(ColumnMetadataManagementListView):
    template_name = "resource_management/column_metadata_management_for_table.html"
    resource_deletion_form_class = ResourceDeletionForm
    multi_resource_deletion_form_class = MultiResourceDeletionForm

    resource_list_reverse = "resource_management:manage_column_metadata"
    new_resource_reverse_base = "resource_management:new_column_metadata"
    resource_update_reverse = "resource_management:update_column_metadata"
    resource_deletion_reverse = "resource_management:delete_column_metadata"
    multi_resource_deletion_reverse = "resource_management:delete_column_metadata_multi"

    def get_field_names_for_table_name(
            self,
            table_name: str,
            updatable_resource_pks: list[str]) -> list[str]:
        if table_name in DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT:
            return list()
        # We want to include the column metadata table's PK fields as these
        # are made up by the "table_name" column and the "column_name" column.
        include_pk_fields = (table_name == "column_metadata")
        form_config_table_name = table_name
        column_metadata_table_name = table_name
        if table_name == TableNames.APPLICATION_NEW:
            column_metadata_table_name = TableNames.APPLICATION
        elif table_name == TableNames.CAPACITY_NEW:
            column_metadata_table_name = TableNames.CAPACITY
        elif table_name == TableNames.APPLICATION:
            # Column metadata table name should be "APPLICATION"
            # but the wizard fields should come from "APPLICATION_NEW".
            form_config_table_name = TableNames.APPLICATION_NEW
        elif table_name == TableNames.CAPACITY:
            # Column metadata table name should be "CAPACITY"
            # but the wizard fields should come from "CAPACITY_NEW".
            form_config_table_name = TableNames.CAPACITY_NEW
        form_config = get_form_config_for_table(
            form_config_table_name,
            self.openapi_spec,
            self.column_metadata,
            column_metadata_table_name=column_metadata_table_name
        )
        return sorted(
            list(form_config.get_fields(
                include_pk_fields=include_pk_fields
            ).keys()),
            key=lambda field_name: f"{table_name}__{field_name}" in updatable_resource_pks
        )

    def get_data_for_resource_update_forms(self) -> dict[str, dict]:
        data = dict()
        for resource in self.resource_list:
            if not (resource.as_dict().get("table_name") == self.current_table_name):
                continue
            data.update({
                get_composite_pk(resource): resource.as_dict(),
            })
        return data

    def get(self, request, *args, **kwargs):
        self.current_table_name = kwargs.get("table_name") or None
        column_metadata = self.api_client.get_endpoint(TableNames.COLUMN_METADATA).get_resources()
        self.resource_list = column_metadata
        self.column_metadata = column_metadata
        self.resources_by_id = {
            get_composite_pk(resource): resource
            for resource in self.resource_list
        }
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
            disabled_properties=[
                "order",
            ]
        )
        ordered_fields_and_categories_for_table_name = get_ordered_fields_and_categories_for_table_name(
            self.current_table_name,
            get_form_config_for_table(
                self.current_table_name,
                self.openapi_spec,
                self.column_metadata
            ),
            self.openapi_spec,
            self.resources_by_id
        )
        context.update({
            "new_resource_reverse_base": self.new_resource_reverse_base,
            "new_resource_form": FormWithDynamicallyPopulatedFields(
                fields=form_config.get_fields()
            ),
            "resource_update_reverse": self.resource_update_reverse,
            "resource_update_form": FormWithDynamicallyPopulatedFields(
                fields=form_config.get_fields()
            ),
            "data_for_resource_update_forms": self.get_data_for_resource_update_forms(),
            "resource_deletion_reverse": self.resource_deletion_reverse,
            "resource_deletion_form": self.resource_deletion_form_class(),
            "multi_resource_deletion_reverse": self.multi_resource_deletion_reverse,
            "multi_resource_deletion_form": self.multi_resource_deletion_form_class(
                resource_ids=[
                    get_composite_pk(resource)
                    for resource in self.resource_list
                    if resource.as_dict().get("table_name") == self.current_table_name
                ]
            ),
            # "resources" are records from the column_metadata table
            "resources": self.resources_by_id,
            "field_names_for_table_name": self.get_field_names_for_table_name(
                self.current_table_name,
                [
                    get_composite_pk(resource)
                    for resource in self.resource_list
                    if resource.as_dict().get("table_name") == self.current_table_name
                ]
            ),
            "ordered_fields_and_categories_for_table_name": ordered_fields_and_categories_for_table_name,
            "current_table_name": self.kwargs["table_name"],
            "category_order_form": CategoryOrderForm(
                initial={"category_order": list(ordered_fields_and_categories_for_table_name.keys())},
            ),
            "field_order_form": FieldOrderForm(
                initial={
                    "field_order": {
                        category_name: [
                            field_name
                            for field_name in field_data.keys()
                        ]
                        for category_name, field_data in ordered_fields_and_categories_for_table_name.items()
                    }
                }
            ),
        })
        return context


class ColumnMetadataFormView(FormView):
    resource_list_reverse_base = "resource_management:manage_column_metadata_for_table"
    column_management_index_url = reverse_lazy("resource_management:manage_column_metadata")

    def form_valid(self, form):
        table_name = self.request.GET.get("table_name")
        if not table_name:
            self.success_url = self.column_management_index_url
            return super().form_valid(form)
        self.success_url = reverse_lazy(
            self.resource_list_reverse_base,
            kwargs={
                "table_name": table_name,
            }
        )
        return super().form_valid(form)

    def redirect_to_resource_list_or_index(self):
        table_name = self.request.GET.get("table_name")
        if not table_name:
            return redirect(self.column_management_index_url)
        return redirect(reverse_lazy(
            self.resource_list_reverse_base,
            kwargs={
                "table_name": table_name,
            }
        ))

    def form_invalid(self, form):
        logger.exception(form.errors.as_json())
        return self.redirect_to_resource_list_or_index()


class NewColumnMetadataFormView(ColumnMetadataFormView):
    form_class = FormWithDynamicallyPopulatedFields
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    table_name = TableNames.COLUMN_METADATA

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        table_name = self.kwargs["table_name"]
        column_name = self.kwargs["column_name"]
        # Ensure current category order isn't affected by the updated column metadata
        # record by recalculating field order for the current table.
        field_order_bulk_update_data = list()
        submitted_category_name = form.cleaned_data.get("category")
        if submitted_category_name:
            column_metadata_by_id = {   
                get_composite_pk(resource): resource
                for resource in self.column_metadata
            }
            order_before_registration = get_ordered_fields_and_categories_for_table_name(
                table_name,
                get_form_config_for_table(
                    table_name,
                    self.openapi_spec,
                    self.column_metadata
                ),
                self.openapi_spec,
                column_metadata_by_id
            )
            field_order_bulk_update_data = get_update_data_for_new_field_order(
                order_before_registration,
                column_metadata_by_id,
                table_name,
                column_name,
                submitted_category_name
            )
        # Register the new column metadata first, then update the field/category
        # order.
        registration_data = form.cleaned_data
        registration_data.update({
            "table_name": table_name,
            "column_name": column_name,
        })
        self.api_client.get_endpoint(
            self.table_name
        ).register_with_composite_key(
            {
                "table_name": table_name,
                "column_name": column_name,
            },
            registration_data
        )

        # Only reassign field order if the bulk update data has been created.
        if field_order_bulk_update_data:
            self.api_client.get_endpoint(
                self.table_name
            ).bulk_update_with_composite_keys(
                field_order_bulk_update_data,
                ["table_name", "column_name"]
            )
        messages.success(
            self.request,
            f"New {humanise_resource_type(self.resource_type)} registered.",
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
        )
        kwargs.update({
            "fields": form_config.get_fields()
        })
        return kwargs


class UpdateColumnMetadataFormView(ColumnMetadataFormView):
    form_class = FormWithDynamicallyPopulatedFields
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    table_name = TableNames.COLUMN_METADATA

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = kwargs["resource_id"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        table_name, column_name = self.resource_id.split("__")
        submitted_category_name = form.cleaned_data.get("category")
        if submitted_category_name:
            column_metadata_by_id = {   
                get_composite_pk(resource): resource
                for resource in self.column_metadata
            }
            order_before_update = get_ordered_fields_and_categories_for_table_name(
                table_name,
                get_form_config_for_table(
                    table_name,
                    self.openapi_spec,
                    self.column_metadata
                ),
                self.openapi_spec,
                column_metadata_by_id
            )
            field_order_bulk_update_data = get_update_data_for_new_field_order(
                order_before_update,
                column_metadata_by_id,
                table_name,
                column_name,
                submitted_category_name
            )
        update_data = form.cleaned_data
        try:
            self.api_client.get_endpoint(self.table_name).update_by_composite_key(
                {
                    "table_name": table_name,
                    "column_name": column_name,
                },
                update_data
            )
        except Exception:
            error_msg = f"An error occurred whilst updating {humanise_resource_type(self.table_name)} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.form_invalid()

        # Only reassign field order if the bulk update data has been created.
        if field_order_bulk_update_data:
            self.api_client.get_endpoint(
                self.table_name
            ).bulk_update_with_composite_keys(
                field_order_bulk_update_data,
                ["table_name", "column_name"]
            )
        message = f"Saved changes to {humanise_resource_type(self.table_name)} {self.resource_id}."
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
        )
        kwargs.update({
            "fields": form_config.get_fields()
        })
        return kwargs


class ColumnMetadataDeletionFormView(ColumnMetadataFormView):
    form_class = ColumnMetadataDeletionForm
    table_name = TableNames.COLUMN_METADATA

    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        resource_id_to_delete = form.cleaned_data.get("resource_id_to_delete")
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        table_name, column_name = resource_id_to_delete.split("__")
        api_client.get_endpoint(self.table_name).delete_by_composite_key({
            "table_name": table_name,
            "column_name": column_name,
        })
        success_msg = f"Deleted {humanise_resource_type(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class MultiColumnMetadataDeletionFormView(ColumnMetadataFormView):
    form_class = MultiResourceDeletionForm
    table_name = TableNames.COLUMN_METADATA

    api_client: ApiClient
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.resource_list = self.api_client.get_endpoint(self.table_name).get_resources()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "resource_ids": [
                get_composite_pk(resource)
                for resource in self.resource_list
            ]
        })
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type_plural(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        delete_conditions = list()
        for resource_id in form.cleaned_data.get("resource_ids_to_delete", []):
            table_name, column_name = resource_id.split("__")
            delete_conditions.append({
                "table_name": table_name,
                "column_name": column_name,
            })
        self.api_client.get_endpoint(self.table_name).delete_many_by_composite_key(
            delete_conditions
        )
        success_msg = f"Deleted 1 {humanise_resource_type(self.resource_type)}."
        if len(delete_conditions) != 1:
            success_msg = f"Deleted {len(delete_conditions)} {humanise_resource_type_plural(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class CategoryOrderFormView(ColumnMetadataFormView):
    form_class = CategoryOrderForm
    table_name = TableNames.COLUMN_METADATA

    api_client: ApiClient
    resource_type: str

    def get_updated_field_order_for_table_by_category_order(
            self,
            table_name: str,
            category_order: list[str]) -> list[dict]:
        update_data = list()
        endpoint = self.api_client.get_endpoint(self.table_name)
        order_number = 0
        DEFAULT_ORDER_NUMBER = 999999
        for category_name in category_order:
            if not category_name:
                continue
            resources = endpoint.get_resources_by_params({
                "table_name": table_name,
                "category": category_name,
            })
            resources_sorted = sorted(
                resources,
                key=lambda resource: (
                    resource.as_dict().get("order")
                    if resource.as_dict().get("order") is not None
                    else DEFAULT_ORDER_NUMBER
                )
            )
            for resource in resources_sorted:
                resource_dict = resource.as_dict()
                update_data.append({
                    "table_name": resource_dict.get("table_name"),
                    "column_name": resource_dict.get("column_name"),
                    "order": order_number,
                })
                order_number += 1
        return update_data

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'The submitted category order data was malformed.',
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        table_name_for_category = self.kwargs.get("table_name") or None
        category_order = form.cleaned_data.get("category_order", list())
        update_data = self.get_updated_field_order_for_table_by_category_order(
            table_name_for_category,
            category_order
        )
        endpoint = self.api_client.get_endpoint(self.table_name)
        endpoint.bulk_update_with_composite_keys(
            update_data,
            ["table_name", "column_name"]
        )
        messages.success(
            self.request,
            f"Updated category order for table."
        )
        return super().form_valid(form)


class FieldOrderFormView(ColumnMetadataFormView):
    form_class = FieldOrderForm
    table_name = TableNames.COLUMN_METADATA

    api_client: ApiClient
    resource_type: str

    def get_updated_field_order_for_table(
            self,
            table_name: str,
            field_order_by_category: dict[str, list[str]]) -> dict[str, list]:
        update_data = list()
        registration_data = list()
        endpoint = self.api_client.get_endpoint(self.table_name)
        order_number = 0
        for category_name, field_pks in field_order_by_category.items():
            if not category_name:
                continue
            resources = endpoint.get_resources_by_params({
                "table_name": table_name,
            })
            resources_by_pk = {
                get_composite_pk(resource): resource
                for resource in resources
            }
            for field_pk in field_pks:
                _table_name, column_name = field_pk.split("__")
                data_for_postgrest = {
                    "table_name": table_name,
                    "column_name": column_name,
                    "order": order_number,
                }
                order_number += 1
                if field_pk in resources_by_pk:
                    update_data.append(data_for_postgrest)
                    continue
                # Column metadata registrations are required to have
                # a title field present.
                data_for_postgrest.update({
                    "title": " ".join(column_name.split("_")).title()
                })
                registration_data.append(data_for_postgrest)
        logger.debug("update_data", update_data)
        logger.debug("registration_data", registration_data)
        return update_data, registration_data

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'The submitted field order data was malformed.',
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        table_name_for_category = self.kwargs.get("table_name") or None
        ordered_field_pks_by_category = form.cleaned_data.get("field_order", dict())
        try:
            update_data, registration_data = self.get_updated_field_order_for_table(
                table_name_for_category,
                ordered_field_pks_by_category,
            )
            endpoint = self.api_client.get_endpoint(self.table_name)
            endpoint.bulk_update_with_composite_keys(
                update_data,
                ["table_name", "column_name"]
            )
            for data in registration_data:
                composite_key = {
                    "table_name": data["table_name"],
                    "column_name": data["column_name"],
                }
                endpoint.register_with_composite_key(
                    composite_key,
                    data
                )
            messages.success(
                self.request,
                f"Updated field order for table."
            )
            return super().form_valid(form)
        except Exception:
            logger.exception("Encountered an error whilst updating field order.")
            messages.error(
                self.request,
                "An unexpected error occurred whilst updating field order. Updates to field order may have been partially applied."
            )
        return self.redirect_to_resource_list_or_index()
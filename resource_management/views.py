import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import FormView, TemplateView, View
from django.views.generic.base import ContextMixin

from .exceptions import NameMissingException, SatBuilderException
from .forms import (
    ColumnMetadataDeletionForm,
    MultiResourceDeletionForm,
    ResourceDeletionForm,
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
def _get_composite_pk(resource: Resource):
    return f"{resource.as_dict().get('table_name')}__{resource.as_dict().get('column_name')}"


class ColumnMetadataManagementListView(TemplateView):
    template_name = "resource_management/column_metadata_management_index.html"
    table_name = TableNames.COLUMN_METADATA
    disabled_table_names = [
        # Column metadata for "APPLICATION_NEW" is stored in "APPLICATION".
        TableNames.APPLICATION_NEW,
        # Column metadata for "CAPACITY_NEW" is stored in "CAPACITY".
        TableNames.CAPACITY_NEW,
        "geography_columns",
        "geometry_columns",
        "spatial_ref_sys",
    ]

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.postgrest_table_names = [
            table_name
            for table_name in self.openapi_spec.get_definitions().keys()
            if table_name not in self.disabled_table_names
        ]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Wizard Customisation",
            "table_names": self.postgrest_table_names,
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
        if table_name in self.disabled_table_names:
            return list()
        # We want to include the column metadata table's PK fields as these
        # are made up by the "table_name" column and the "column_name" column.
        include_pk_fields = (table_name == "column_metadata")
        column_metadata_table_name = table_name
        if table_name == TableNames.APPLICATION_NEW:
            column_metadata_table_name = TableNames.APPLICATION
        if table_name == TableNames.CAPACITY_NEW:
            column_metadata_table_name = TableNames.CAPACITY
        form_config = get_form_config_for_table(
            table_name,
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

    def get_field_order_by_category_for_table_name(self, table_name) -> dict[str, dict]:
        if table_name in self.disabled_table_names:
            return dict()
        UNCATEGORISED = "Unknown"
        DEFAULT_ORDER_NUMBER = 999999
        column_metadata_by_category = {
            UNCATEGORISED: dict(),
        }
        for resource in self.column_metadata:
            cm_table_name = resource.as_dict().get("table_name", "")
            if cm_table_name != table_name:
                continue
            category = resource.as_dict().get("category", "")
            order_number = resource.as_dict().get("order", DEFAULT_ORDER_NUMBER)
            if not isinstance(order_number, int):
                order_number = DEFAULT_ORDER_NUMBER
            if not category or len(category.strip()) == 0:
                column_metadata_by_category[UNCATEGORISED].update({
                    _get_composite_pk(resource): {"order": order_number},
                })
                continue
            if category not in column_metadata_by_category:
                column_metadata_by_category.update({
                    category: dict(),
                })
            column_metadata_by_category[category].update({
                _get_composite_pk(resource): {"order": order_number},
            })
        return column_metadata_by_category

    def get_ordered_fields_and_categories_for_table_name(self, table_name: str) -> dict:
        if (table_name not in self.postgrest_table_names
            or table_name in self.disabled_table_names):
            return dict()
        
        data = dict()
        DEFAULT_ORDER_NUMBER = 999999

        field_order_by_category = self.get_field_order_by_category_for_table_name(table_name)
        # Format category order as a list to make it easier to sort.
        category_order = [
            {
                "category": category_name,
                "order": max(
                    field_order.values(),
                    key=lambda data: data.get("order", DEFAULT_ORDER_NUMBER),
                    default={"order": DEFAULT_ORDER_NUMBER}
                ).get("order")
            }
            for category_name, field_order in field_order_by_category.items()
        ]
        data = {
            order_data["category"]: field_order_by_category.get(
                order_data["category"],
                dict()
            )
            for order_data in sorted(
                category_order,
                key=lambda order_data: order_data["order"]
            )
        }

        UNCATEGORISED = "Unknown"
        # We want to include the column metadata table's PK fields as these
        # are made up by the "table_name" column and the "column_name" column.
        include_pk_fields = (table_name == "column_metadata")
        form_config = get_form_config_for_table(
            table_name,
            self.openapi_spec,
            self.column_metadata
        )
        fields_names = form_config.get_fields(include_pk_fields=include_pk_fields).keys()
        for field_name in fields_names:
            # These dict keys should match the stringified composite key
            # format of the column metadata records ({table_name}__{column_name}).
            possible_resource_pk = f"{table_name}__{field_name}"
            # If the resource PK already has some column metadata assigned, there's no
            # need to add it again.
            if possible_resource_pk in self.resources_by_id:
                continue
            data[UNCATEGORISED].update({
                possible_resource_pk: {"order": DEFAULT_ORDER_NUMBER}
            })

        for category_name, field_order in data.items():
            data.update({
                category_name: {
                    key: field_dict
                    for key, field_dict in sorted(
                        list(field_order.items()),
                        key=lambda field_item: field_item[1].get("order")
                    )
                }
            })

        return data

    def get_data_for_resource_update_forms(self) -> dict[str, dict]:
        data = dict()
        for resource in self.resource_list:
            if not (resource.as_dict().get("table_name") == self.current_table_name):
                continue
            data.update({
                _get_composite_pk(resource): resource.as_dict(),
            })
        return data

    def get(self, request, *args, **kwargs):
        self.current_table_name = kwargs.get("table_name") or None
        column_metadata = self.api_client.get_endpoint(TableNames.COLUMN_METADATA).get_resources()
        self.resource_list = column_metadata
        self.column_metadata = column_metadata
        self.resources_by_id = {
            _get_composite_pk(resource): resource
            for resource in self.resource_list
        }
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
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
                    _get_composite_pk(resource)
                    for resource in self.resource_list
                    if resource.as_dict().get("table_name") == self.current_table_name
                ]
            ),
            # "resources" are records from the column_metadata table
            "resources": self.resources_by_id,
            "field_names_for_table_name": self.get_field_names_for_table_name(
                self.current_table_name,
                [
                    _get_composite_pk(resource)
                    for resource in self.resource_list
                    if resource.as_dict().get("table_name") == self.current_table_name
                ]
            ),
            "ordered_fields_and_categories_for_table_name": self.get_ordered_fields_and_categories_for_table_name(
                self.current_table_name
            ),
            "current_table_name": self.kwargs["table_name"],
        })
        return context


class ColumnMetadataFormView(FormView):
    resource_list_reverse_base = "resource_management:manage_column_metadata_for_table"

    def form_valid(self, form):
        table_name = self.request.GET.get("table_name")
        self.success_url = reverse_lazy(
            self.resource_list_reverse_base,
            kwargs={
                "table_name": table_name,
            }
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        table_name = self.request.GET.get("table_name")
        return redirect(
            self.resource_list_reverse_base,
            kwargs={
                "table_name": table_name,
            }
        )


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
        update_data = form.cleaned_data
        try:
            table_name, column_name = self.resource_id.split("__")
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
                _get_composite_pk(resource)
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

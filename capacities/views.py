from django.urls import reverse_lazy

from .tosca import generate_capacity_description_template
from .view_helpers import (
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.views import (
    EditorOverviewTemplateView,
    EditorStartFormView,
    EditorView,
    UpdateResourceByCategoryView,
)
from postgrest.new_api import ApiClient
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListFormView,
    ToscaTemplateDownloadView,
)


# Cloud Capacity (CC)
class CloudCapacityEditorView(CloudCapacityViewMixin, EditorView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]
    resource_type = "cloud_capacity"
    editor_form_reverse = "capacities:update_cloud_capacity_by_category"


class UpdateCloudCapacityByCategoryView(CloudCapacityViewMixin, UpdateResourceByCategoryView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


class CloudCapacityEditorStartFormView(CloudCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_cloud_capacity_start.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]

    def get_registration_data(self, form) -> dict:
        registration_data = super().get_registration_data(form)
        registration_data.update({
            "resource_type": "Cloud",
        })
        return registration_data


class CloudCapacityEditorOverviewTemplateView(CloudCapacityViewMixin, EditorOverviewTemplateView):
    template_name = "capacities/cloud_capacity_overview.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


# Resource management views (CC)
class CloudCapacityDeletionFormView(CloudCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")
    table_name = "capacity_new"


class MultiCloudCapacityDeletionFormView(CloudCapacityViewMixin, MultiResourceDeletionFormView):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")
    table_name = "capacity_new"


class CloudCapacityListFormView(CloudCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/cloud_capacities.html"
    table_name = "capacity_new"

    def get_resource_list(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        return api_client.get_endpoint("capacity_new").get_resources_by_type("Cloud")


class CloudCapacityDescriptionTemplateDownloadView(
        CloudCapacityViewMixin,
        ToscaTemplateDownloadView):
    table_name = "capacity_new"

    def generate_tosca_template(self):
        return generate_capacity_description_template(self.resource_id)


# Edge Capacity views (EC)
class EdgeCapacityEditorView(EdgeCapacityViewMixin, EditorView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]
    resource_type = "edge_capacity"
    editor_form_reverse = "capacities:update_edge_capacity_by_category"


class UpdateEdgeCapacityByCategoryView(EdgeCapacityViewMixin, UpdateResourceByCategoryView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]


class EdgeCapacityEditorStartFormView(EdgeCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]

    def get_registration_data(self, form) -> dict:
        registration_data = super().get_registration_data(form)
        registration_data.update({
            "resource_type": "Edge",
        })
        return registration_data


class EdgeCapacityEditorOverviewTemplateView(EdgeCapacityViewMixin, EditorOverviewTemplateView):
    template_name = "capacities/edge_capacity_overview.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]


# Resource management views (EC)
class EdgeCapacityDeletionFormView(EdgeCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")
    table_name = "capacity_new"


class MultiEdgeCapacityDeletionFormView(EdgeCapacityViewMixin, MultiResourceDeletionFormView):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_edge_capacities")
    table_name = "capacity_new"


class EdgeCapacityListFormView(EdgeCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/edge_capacities.html"
    table_name = "capacity_new"

    def get_resource_list(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        return api_client.get_endpoint("capacity_new").get_resources_by_type("Edge")


class EdgeCapacityDescriptionTemplateDownloadView(
        EdgeCapacityViewMixin,
        ToscaTemplateDownloadView):
    table_name = "capacity_new"

    def generate_tosca_template(self):
        return generate_capacity_description_template(self.resource_id)
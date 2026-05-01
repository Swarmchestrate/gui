from django.urls import reverse_lazy

from .view_helpers import (
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.views import (
    EditorOverviewTemplateView,
    EditorSkeletonLoaderView,
    EditorStartFormView,
    EditorTableOfContentsSectionView,
    EditorTabSectionView,
    UpdateResourceByCategoryView,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListFormView,
)


# Cloud Capacity (CC)
class CloudCapacityEditorSkeletonLoaderView(CloudCapacityViewMixin, EditorSkeletonLoaderView):
    table_name = "capacity_new"
    template_name = "capacities/cloud_capacity_editor.html"
    success_url = reverse_lazy("capacities:new_cloud_capacity")
    toc_url = reverse_lazy("capacities:cloud_capacity_editor_toc")
    tabbed_form_reverse = "capacities:cloud_capacity_editor_tabbed_form"


class CloudCapacityEditorTableOfContentsView(EditorTableOfContentsSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


class CloudCapacityEditorTabSectionView(CloudCapacityViewMixin, EditorTabSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]
    editor_form_reverse = "capacities:update_cloud_capacity_by_category"
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class UpdateCloudCapacityByCategoryView(CloudCapacityViewMixin, UpdateResourceByCategoryView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


class CloudCapacityEditorStartFormView(CloudCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_cloud_capacity_start.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


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


# Edge Capacity views (EC)
class EdgeCapacityEditorSkeletonLoaderView(EdgeCapacityViewMixin, EditorSkeletonLoaderView):
    table_name = "capacity_new"
    template_name = "capacities/edge_capacity_editor.html"
    success_url = reverse_lazy("capacities:new_edge_capacity")
    toc_url = reverse_lazy("capacities:edge_capacity_editor_toc")
    tabbed_form_reverse = "capacities:edge_capacity_editor_tabbed_form"


class EdgeCapacityTableOfContentsView(EditorTableOfContentsSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]


class EdgeCapacityEditorTabSectionView(EdgeCapacityViewMixin, EditorTabSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]
    editor_form_reverse = "capacities:update_edge_capacity_by_category"
    new_one_to_one_relation_reverse_base = "capacities:new_edge_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_edge_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_edge_capacity_one_to_one_relation"
    new_one_to_many_relation_reverse_base = "capacities:new_edge_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_edge_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_edge_capacity_one_to_many_relation"


class UpdateEdgeCapacityByCategoryView(EdgeCapacityViewMixin, UpdateResourceByCategoryView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]


class EdgeCapacityEditorStartFormView(EdgeCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    disabled_categories = ["System Specific"]


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
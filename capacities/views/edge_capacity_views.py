from django.urls import reverse_lazy

from capacities.utils import (
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
)
from editor.new_foreign_key_views import (
    DeleteOneToManyRelationFormView,
    DeleteOneToOneRelationFormView,
    NewOneToManyRelationFormView,
    NewOneToOneRelationFormView,
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)
from editor.new_views import (
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


# Edge Capacity
class EdgeCapacityViewMixin:
    editor_reverse_base = "capacities:edge_capacity_editor"
    editor_start_reverse_base = "capacities:new_edge_capacity"
    editor_overview_reverse_base = "capacities:edge_capacity_overview"
    resource_list_reverse = "capacities:edge_capacity_list"
    new_resource_reverse = "capacities:new_edge_capacity"
    resource_deletion_reverse = "capacities:delete_edge_capacity"
    multi_resource_deletion_reverse = "capacities:delete_edge_capacities"
    resource_type_readable = edge_capacity_type_readable()
    resource_type_readable_plural = edge_capacity_type_readable_plural()


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


class EdgeCapacityEditorTabSectionView(EditorTabSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
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


class EdgeCapacityEditorStartFormView(EdgeCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"


class EdgeCapacityDeletionFormView(EdgeCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class MultiEdgeCapacityDeletionFormView(EdgeCapacityViewMixin, MultiResourceDeletionFormView):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_edge_capacities")


class EdgeCapacityListFormView(EdgeCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/edge_capacities.html"
    table_name = "capacity_new"


class EdgeCapacityEditorOverviewTemplateView(EdgeCapacityViewMixin, EditorOverviewTemplateView):
    template_name = "capacities/edge_capacity_overview.html"

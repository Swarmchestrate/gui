from dataclasses import dataclass

from django.urls import reverse_lazy
from django.views.generic import TemplateView

from capacities.forms.cloud_capacity_forms import (
    CloudCapacityCategoryBasedEditorForm,
    CloudCapacityEditorForm,
    CloudCapacityRegistrationForm,
)
from capacities.utils import (
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
)

from editor.new_views import (
    EditorSkeletonLoaderView,
    UpdateResourceByCategoryView,
    EditorOverviewTemplateView,
    EditorTableOfContentsSectionView,
    EditorTabSectionView,
    EditorStartFormView,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListFormView,
)


# Cloud Capacity
@dataclass
class CloudCapacityViewMixin:
    table_name = 'cloud_capacity'
    editor_reverse_base = "capacities:cloud_capacity_editor"
    editor_start_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_reverse_base = "capacities:cloud_capacity_overview"
    resource_list_reverse = "capacities:cloud_capacity_list"
    new_resource_reverse = "capacities:new_cloud_capacity"
    resource_deletion_reverse = "capacities:delete_cloud_capacity"
    multi_resource_deletion_reverse = "capacities:delete_cloud_capacities"
    resource_type_readable = cloud_capacity_type_readable()
    resource_type_readable_plural = cloud_capacity_type_readable_plural()


class CloudCapacityEditorSkeletonLoaderView(CloudCapacityViewMixin, EditorSkeletonLoaderView):
    table_name = "capacity_new"
    template_name = "capacities/cloud_capacity_editor.html"
    success_url = reverse_lazy("capacities:new_cloud_capacity")
    toc_url = reverse_lazy("capacities:cloud_capacity_editor_toc")
    tabbed_form_reverse = "capacities:cloud_capacity_editor_tabbed_form"


class CloudCapacityEditorTableOfContentsView(EditorTableOfContentsSectionView):
    table_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


class CloudCapacityEditorTabSectionView(EditorTabSectionView):
    table_name = "capacity_new"
    column_metadata_table_name = "capacity"
    editor_form_reverse = "capacities:update_cloud_capacity_by_category"
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class UpdateCloudCapacityByCategoryView(CloudCapacityViewMixin, UpdateResourceByCategoryView):
    table_name = "capacity"


class CloudCapacityEditorStartFormView(CloudCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_cloud_capacity_start.html"
    table_name = "capacity"


# Resource management views
class CloudCapacityDeletionFormView(CloudCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class MultiCloudCapacityDeletionFormView(CloudCapacityViewMixin, MultiResourceDeletionFormView):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class CloudCapacityListFormView(CloudCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/cloud_capacities.html"


class CloudCapacityEditorOverviewTemplateView(CloudCapacityViewMixin, EditorOverviewTemplateView):
    template_name = "capacities/cloud_capacity_overview.html"


class CloudCapacityNewOneToOneRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToOneRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToOneRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityNewOneToManyRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToManyRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToManyRelationFormView(
    CloudCapacityViewMixin, TemplateView
):
    template_name = "capacities/cloud_capacity_editor.html"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)

from django.urls import path

from . import views

app_name = "instance_types"

urlpatterns = [
    path(
        "instance-types/",
        views.InstanceTypeListFormView.as_view(),
        name="instance_type_list",
    ),
    path(
        "instance-types/new/",
        views.InstanceTypeEditorStartFormView.as_view(),
        name="new_instance_type",
    ),
    path(
        "instance-types/<resource_id>/overview/",
        views.InstanceTypeEditorOverviewTemplateView.as_view(),
        name="instance_type_overview",
    ),
    path(
        "instance-types/<resource_id>/edit/",
        views.InstanceTypeEditorProcessFormView.as_view(),
        name="instance_type_editor",
    ),
]

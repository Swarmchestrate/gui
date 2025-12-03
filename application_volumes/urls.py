from django.urls import path

from . import views

app_name = "application_volumes"

urlpatterns = [
    path(
        "application-volumes/",
        views.ApplicationVolumeListFormView.as_view(),
        name="application_volume_list",
    ),
    path(
        "application-volumes/new/",
        views.NewApplicationVolumeFormView.as_view(),
        name="new_application_volume",
    ),
    path(
        "application-volumes/deletes/",
        views.MultiApplicationVolumeDeletionFormView.as_view(),
        name="delete_application_volumes",
    ),
    path(
        "application-volumes/<resource_id>/edit/",
        views.ApplicationVolumeUpdateFormView.as_view(),
        name="update_application_volume",
    ),
    path(
        "application-volumes/<resource_id>/delete/",
        views.ApplicationVolumeDeletionFormView.as_view(),
        name="delete_application_volume",
    ),
]

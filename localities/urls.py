from django.urls import path

from . import views

app_name = "localities"

urlpatterns = [
    path(
        "localities/",
        views.LocalityListFormView.as_view(),
        name="locality_list",
    ),
    path(
        "localities/new/",
        views.LocalityEditorStartFormView.as_view(),
        name="new_locality",
    ),
    path(
        "localities/deletes/",
        views.LocalityDeletionFormView.as_view(),
        name="delete_localities",
    ),
    path(
        "localities/<resource_id>/edit/",
        views.LocalityUpdateFormView.as_view(),
        name="update_locality",
    ),
    path(
        "api/localities/search/",
        views.CapacityLocalityOptionsSearchProcessFormView.as_view(),
        name="locality_options_search",
    ),
    path(
        "api/localities/by-name/",
        views.CapacityGetLocalityByNameProcessFormView.as_view(),
        name="get_locality_by_name",
    ),
    path(
        "api/localities/by-gps/",
        views.CapacityGetLocalityByGpsProcessFormView.as_view(),
        name="get_locality_by_gps",
    ),
]

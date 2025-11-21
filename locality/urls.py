from django.urls import path

from . import views

app_name = "locality"

urlpatterns = [
    path(
        "api/locality/search",
        views.CapacityLocalityOptionsSearchProcessFormView.as_view(),
        name="locality_options_search",
    ),
    path(
        "api/locality-by-name/",
        views.CapacityGetLocalityByNameProcessFormView.as_view(),
        name="get_locality_by_name",
    ),
    path(
        "api/locality-by-gps/",
        views.CapacityGetLocalityByGpsProcessFormView.as_view(),
        name="get_locality_by_gps",
    ),
]

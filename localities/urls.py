from django.urls import path

from . import views

app_name = "localities"

urlpatterns = [
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

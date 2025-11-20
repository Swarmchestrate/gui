from django.urls import path

from .views import locality_views

app_name = "editor"

urlpatterns = [
    path(
        "api/locality/search",
        locality_views.CapacityLocalityOptionsSearchProcessFormView.as_view(),
        name="locality_options_search",
    ),
    path(
        "api/locality-by-name/",
        locality_views.CapacityGetLocalityByNameProcessFormView.as_view(),
        name="get_locality_by_name",
    ),
    path(
        "api/locality-by-gps/",
        locality_views.CapacityGetLocalityByGpsProcessFormView.as_view(),
        name="get_locality_by_gps",
    ),
]

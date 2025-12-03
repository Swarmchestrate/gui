from django.urls import path

from . import views

app_name = "application_pref_resource_providers"

urlpatterns = [
    path(
        "application-pref-resource-providers/",
        views.ApplicationPrefResourceProviderListFormView.as_view(),
        name="application_pref_resource_provider_list",
    ),
    path(
        "application-pref-resource-providers/new/",
        views.NewApplicationPrefResourceProviderFormView.as_view(),
        name="new_application_pref_resource_provider",
    ),
    path(
        "application-pref-resource-providers/deletes/",
        views.MultiApplicationPrefResourceProviderDeletionFormView.as_view(),
        name="delete_application_pref_resource_providers",
    ),
    path(
        "application-pref-resource-providers/<resource_id>/edit/",
        views.ApplicationPrefResourceProviderUpdateFormView.as_view(),
        name="update_application_pref_resource_provider",
    ),
    path(
        "application-pref-resource-providers/<resource_id>/delete/",
        views.ApplicationPrefResourceProviderDeletionFormView.as_view(),
        name="delete_application_pref_resource_provider",
    ),
]

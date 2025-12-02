from django.urls import path

from . import views

app_name = "application_behaviours"

urlpatterns = [
    path(
        "application-behaviours/",
        views.ApplicationBehaviourListFormView.as_view(),
        name="application_behaviour_list",
    ),
    path(
        "application-behaviours/new/",
        views.NewApplicationBehaviourFormView.as_view(),
        name="new_application_behaviour",
    ),
    path(
        "application-behaviours/deletes/",
        views.MultiApplicationBehaviourDeletionFormView.as_view(),
        name="delete_application_behaviours",
    ),
    path(
        "application-behaviours/<resource_id>/edit/",
        views.ApplicationBehaviourUpdateFormView.as_view(),
        name="update_application_behaviour",
    ),
    path(
        "application-behaviours/<resource_id>/delete/",
        views.ApplicationBehaviourDeletionFormView.as_view(),
        name="delete_application_behaviour",
    ),
]

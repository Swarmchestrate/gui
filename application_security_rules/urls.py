from django.urls import path

from . import views

app_name = "application_security_rules"

urlpatterns = [
    path(
        "application-security-rules/",
        views.ApplicationSecurityRuleListFormView.as_view(),
        name="application_security_rule_list",
    ),
    path(
        "application-security-rules/new/",
        views.NewApplicationSecurityRuleFormView.as_view(),
        name="new_application_security_rule",
    ),
    path(
        "application-security-rules/deletes/",
        views.MultiApplicationSecurityRuleDeletionFormView.as_view(),
        name="delete_application_security_rules",
    ),
    path(
        "application-security-rules/<resource_id>/edit/",
        views.ApplicationSecurityRuleUpdateFormView.as_view(),
        name="update_application_security_rule",
    ),
    path(
        "application-security-rules/<resource_id>/delete/",
        views.ApplicationSecurityRuleDeletionFormView.as_view(),
        name="delete_application_security_rule",
    ),
]

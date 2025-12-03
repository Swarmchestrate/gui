from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
)
from resource_management.views import (
    BasicResourceListFormView,
    MultiResourceDeletionFormView,
    NewResourceFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceUpdateFormView,
)

# from .api.api_clients import (
#     ApplicationSecurityRuleApiClient,
#     ApplicationSecurityRuleColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationSecurityRuleApiClient,
    ApplicationSecurityRuleColumnMetadataApiClient,
)
from .forms import (
    ApplicationSecurityRuleRegistrationForm,
    ApplicationSecurityRuleUpdateForm,
)
from .utils import (
    application_security_rule_type_readable,
    application_security_rule_type_readable_plural,
)


# Create your views here.
class ApplicationSecurityRuleViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationSecurityRuleApiClient
    column_metadata_api_client_class = ApplicationSecurityRuleColumnMetadataApiClient
    resource_list_reverse = "application_security_rules:application_security_rule_list"
    resource_update_reverse = (
        "application_security_rules:update_application_security_rule"
    )
    new_resource_reverse = "application_security_rules:new_application_security_rule"
    resource_deletion_reverse = (
        "application_security_rules:delete_application_security_rule"
    )
    multi_resource_deletion_reverse = (
        "application_security_rules:delete_application_security_rules"
    )
    resource_type_readable = application_security_rule_type_readable()
    resource_type_readable_plural = application_security_rule_type_readable_plural()


class ApplicationSecurityRuleListFormView(
    ApplicationSecurityRuleViewMixin, BasicResourceListFormView
):
    template_name = "application_security_rules/application_security_rules.html"
    new_resource_form_class = ApplicationSecurityRuleRegistrationForm
    resource_update_form_class = ApplicationSecurityRuleUpdateForm


class NewApplicationSecurityRuleFormView(
    ApplicationSecurityRuleViewMixin, NewResourceFormView
):
    template_name = "application_security_rules/application_security_rules.html"
    new_resource_form_class = ApplicationSecurityRuleRegistrationForm
    resource_update_form_class = ApplicationSecurityRuleUpdateForm
    form_class = ApplicationSecurityRuleRegistrationForm


class ApplicationSecurityRuleUpdateFormView(
    ApplicationSecurityRuleViewMixin, ResourceUpdateFormView
):
    template_name = "application_security_rules/application_security_rules.html"
    new_resource_form_class = ApplicationSecurityRuleRegistrationForm
    resource_update_form_class = ApplicationSecurityRuleUpdateForm
    form_class = ApplicationSecurityRuleUpdateForm


class ApplicationSecurityRuleDeletionFormView(
    ApplicationSecurityRuleViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationSecurityRuleDeletionFormView(
    ApplicationSecurityRuleViewMixin, MultiResourceDeletionFormView
):
    pass

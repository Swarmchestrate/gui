from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix


class ApplicationSecurityRuleRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_security_rule"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationSecurityRuleUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "application_security_rule"

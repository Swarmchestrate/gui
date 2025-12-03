from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix


class ApplicationPrefResourceProviderRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_pref_resource_provider"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationPrefResourceProviderUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "application_pref_resource_provider"

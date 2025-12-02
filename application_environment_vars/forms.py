from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix


class ApplicationEnvironmentVarRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_environment_var"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationEnvironmentVarUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "application_environment_var"

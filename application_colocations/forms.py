from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix


class ApplicationColocationRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_colocate"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationColocationUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "application_colocate"

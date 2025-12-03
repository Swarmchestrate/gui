from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix


class ApplicationVolumeRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_volume"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationVolumeUpdateForm(OpenApiSpecificationBasedFormWithIdAttributeSuffix):
    definition_name = "application_volume"

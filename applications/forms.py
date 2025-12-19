from editor.forms.base_forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "application"


class ApplicationEditorForm(OpenApiSpecificationBasedForm):
    definition_name = "application"

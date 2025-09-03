from editor.forms import (
    OpenApiSpecificationFieldFormatBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'application'


class ApplicationEditorForm(OpenApiSpecificationFieldFormatBasedForm):
    definition_name = 'application'
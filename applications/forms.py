from editor.forms import (
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'application'


class ApplicationEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'application'

from editor.forms.base_forms import (
    LocalityEditorForm,
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'application'


class ApplicationEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'application'


class ApplicationLocalityEditorForm(LocalityEditorForm):
    pass

from editor.forms.base_forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
    OpenApiSpecificationCategoryBasedForm,
)


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "application"


class ApplicationEditorForm(OpenApiSpecificationBasedForm):
    definition_name = "application"


class ApplicationCategoryBasedEditorForm(OpenApiSpecificationBasedForm):
    definition_name = "application"

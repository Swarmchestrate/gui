from editor.forms.base_forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)
from localities.forms import LocalityEditorForm


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "application"


class ApplicationEditorForm(OpenApiSpecificationBasedForm):
    definition_name = "application"


class ApplicationLocalityEditorForm(LocalityEditorForm):
    pass

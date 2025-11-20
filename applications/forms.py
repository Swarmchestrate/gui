from editor.forms.base_forms import (
    OpenApiSpecificationBasedRegistrationForm,
    OpenApiSpecificationCategoryBasedForm,
)
from editor.forms.helpers.locality_forms import LocalityEditorForm


class ApplicationRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "application"


class ApplicationEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = "application"


class ApplicationLocalityEditorForm(LocalityEditorForm):
    pass

from editor.forms import (
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class CloudCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class CloudCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'


class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class EdgeCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'

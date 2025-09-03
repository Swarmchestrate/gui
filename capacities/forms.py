from editor.forms import (
    OpenApiSpecificationFieldFormatBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class CloudCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class CloudCapacityEditorForm(OpenApiSpecificationFieldFormatBasedForm):
    definition_name = 'capacity'


class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class EdgeCapacityEditorForm(OpenApiSpecificationFieldFormatBasedForm):
    definition_name = 'capacity'
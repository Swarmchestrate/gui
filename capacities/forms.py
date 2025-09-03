from editor.forms import (
    OpenApiSpecificationFieldFormatBasedForm,
    OpenApiSpecificationSpecifiedFieldsBasedForm,
)


class CloudCapacityRegistrationForm(OpenApiSpecificationSpecifiedFieldsBasedForm):
    definition_name = 'capacity'


class CloudCapacityEditorForm(OpenApiSpecificationFieldFormatBasedForm):
    definition_name = 'capacity'


class EdgeCapacityEditorForm(OpenApiSpecificationFieldFormatBasedForm):
    definition_name = 'capacity'
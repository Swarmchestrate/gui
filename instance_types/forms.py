from editor.forms import (
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class InstanceTypeRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'instance_type'


class InstanceTypeEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'instance_type'

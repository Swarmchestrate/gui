from django import forms

from .api_endpoint_client import (
    InstanceTypeApiEndpointClient,
    InstanceTypeColumnMetadataApiEndpointClient,
)

from editor.forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class InstanceTypeRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'instance_type'


class InstanceTypeEditorForm(OpenApiSpecificationBasedForm):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InstanceTypeApiEndpointClient(),
            InstanceTypeColumnMetadataApiEndpointClient(),
            *args,
            **kwargs
        )
    definition_name = 'instance_type'

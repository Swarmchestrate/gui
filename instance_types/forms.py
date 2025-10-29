from django import forms

from .api_endpoint_client import (
    InstanceTypeApiEndpointClient,
    InstanceTypeColumnMetadataApiEndpointClient,
)

from editor.forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class InstanceTypeRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'instance_type'


class InstanceTypeEditorForm(OpenApiSpecificationBasedForm):
    def __init__(self, *args, **kwargs):
        instance_type_endpoint_client = InstanceTypeApiEndpointClient()
        super().__init__(
            instance_type_endpoint_client,
            InstanceTypeColumnMetadataApiEndpointClient(),
            *args,
            **kwargs
        )
        self.fields[instance_type_endpoint_client.endpoint_definition.id_field] = forms.IntegerField(
            required=False,
            widget=forms.HiddenInput()
        )
    definition_name = 'instance_type'

    unsaved = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'class': 'unsaved-flag',
        })
    )

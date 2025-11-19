from django import forms

from editor.forms.base_forms import (
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)
from editor.forms.widget_choices import (
    disk_size_choices,
    mem_size_choices,
    num_cpus_choices,
)

# from .api.endpoints.instance_type import (
#     InstanceTypeApiEndpoint,
#     InstanceTypeColumnMetadataApiEndpoint,
# )
from .mocks.endpoints.instance_type import (
    InstanceTypeApiEndpoint,
    InstanceTypeColumnMetadataApiEndpoint,
)


class InstanceTypeRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "instance_type"


class InstanceTypeEditorForm(OpenApiSpecificationBasedForm):
    widget_enhancements = {
        "num_cpus": forms.Select(
            choices=num_cpus_choices(), attrs={"class": "form-select"}
        ),
        "mem_size": forms.Select(
            choices=mem_size_choices(), attrs={"class": "form-select"}
        ),
        "disk_size": forms.Select(
            choices=disk_size_choices(), attrs={"class": "form-select"}
        ),
    }

    def __init__(self, *args, **kwargs):
        instance_type_endpoint_client = InstanceTypeApiEndpoint()
        super().__init__(
            instance_type_endpoint_client,
            InstanceTypeColumnMetadataApiEndpoint(),
            *args,
            **kwargs,
        )
        self.fields[instance_type_endpoint_client.endpoint_definition.id_field] = (
            forms.IntegerField(required=False, widget=forms.HiddenInput())
        )
        # Add widget enhancements
        for field_name, widget in self.widget_enhancements.items():
            if field_name not in self.fields:
                continue
            self.fields[field_name].widget = widget

    definition_name = "instance_type"

    unsaved = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "unsaved-flag",
            }
        ),
    )

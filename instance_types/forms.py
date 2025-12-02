from django import forms

from editor.forms.base_forms import OpenApiSpecificationBasedForm
from editor.forms.widget_choices import (
    disk_size_choices,
    mem_size_choices,
    num_cpus_choices,
)
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     InstanceTypeApiClient,
#     InstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    InstanceTypeApiClient,
    InstanceTypeColumnMetadataApiClient,
)


class InstanceTypeRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "locality"

    def add_prefix(self, field_name):
        return "new-" + field_name


class InstanceTypeUpdateForm(OpenApiSpecificationBasedFormWithIdAttributeSuffix):
    definition_name = "locality"


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
        instance_type_api_client = InstanceTypeApiClient()
        super().__init__(
            instance_type_api_client,
            InstanceTypeColumnMetadataApiClient(),
            *args,
            **kwargs,
        )
        self.fields[instance_type_api_client.endpoint_definition.id_field] = (
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

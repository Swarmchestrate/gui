from django import forms

from editor.forms.base_forms import OpenApiSpecificationBasedForm
from editor.forms.widget_choices import (
    disk_size_choices,
    mem_size_choices,
    num_cpus_choices,
)
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     CapacityInstanceTypeApiClient,
#     CapacityInstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityInstanceTypeApiClient,
    CapacityInstanceTypeColumnMetadataApiClient,
)


class CapacityInstanceTypeRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_instance_type"

    def add_prefix(self, field_name):
        return "new-" + field_name


class CapacityInstanceTypeUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "capacity_instance_type"


class CapacityInstanceTypeEditorForm(OpenApiSpecificationBasedForm):
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
        capacity_instance_type_api_client = CapacityInstanceTypeApiClient()
        super().__init__(
            capacity_instance_type_api_client,
            CapacityInstanceTypeColumnMetadataApiClient(),
            *args,
            **kwargs,
        )
        self.fields[capacity_instance_type_api_client.endpoint_definition.id_field] = (
            forms.IntegerField(required=False, widget=forms.HiddenInput())
        )
        # Add widget enhancements
        for field_name, widget in self.widget_enhancements.items():
            if field_name not in self.fields:
                continue
            self.fields[field_name].widget = widget

    definition_name = "capacity_instance_type"

    unsaved = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "unsaved-flag",
            }
        ),
    )

from django import forms

from editor.forms.base_forms import (
    EditorForm,
    OpenApiSpecificationBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


# Edge Capacity forms
class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "capacity_new"


class EdgeCapacityEditorForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_new"


# Forms to be used in formsets to help with the input
# of certain fields.
class EdgeCapacityAccessibleSensorsEditorForm(EditorForm):
    sensor_name = forms.CharField(
        label="Sensor Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )


class EdgeCapacityDevicesEditorForm(EditorForm):
    device_type = forms.ChoiceField(
        label="Device Type",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
        choices=[
            ("", ""),
            ("hardware", "Hardware"),
            ("software", "Software"),
        ],
        required=True,
    )

    device_name = forms.CharField(
        label="Device Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )

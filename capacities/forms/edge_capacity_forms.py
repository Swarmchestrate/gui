from django import forms

from editor.forms.base_forms import (
    EditorForm,
    OpenApiSpecificationBasedRegistrationForm,
    OpenApiSpecificationCategoryBasedForm,
)


# Edge Capacity forms
class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "capacity"


class EdgeCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = "capacity"


# Sub-forms to faciliate input for certain fields
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

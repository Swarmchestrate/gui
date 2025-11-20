from django import forms

from editor.forms.base_forms import (
    EditorForm,
    OpenApiSpecificationBasedRegistrationForm,
    OpenApiSpecificationCategoryBasedForm,
)


# Cloud Capacity forms
class CloudCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = "capacity"


class CloudCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = "capacity"
    disabled_categories = ["Edge Specific", "Networking"]


# Forms to be used in formsets to help with the input
# of certain fields.
class CloudCapacityArchitectureEditorForm(EditorForm):
    architecture_name = forms.CharField(
        label="Architecture Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )


class CloudCapacityOperatingSystemEditorForm(EditorForm):
    os_name = forms.CharField(
        label="OS Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )

    os_id = forms.CharField(
        label="OS Identifier",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )

from django import forms

from editor.forms.base_forms import EditorForm
from localities.forms import LocalityEditorForm


# Cloud & Edge Capacity forms
class CapacityPriceEditorForm(EditorForm):
    instance_type = forms.CharField(
        label="Instance Type",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        required=True,
    )

    credits_per_hour = forms.FloatField(
        label="Cost (Credits per Hour)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.0001",
            }
        ),
        required=True,
    )


class CapacityEnergyConsumptionEditorForm(EditorForm):
    type = forms.CharField(
        label="Type",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="E.g. CPU-based",
        required=True,
    )

    amount = forms.CharField(
        label="Energy Consumed",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="E.g. 5W",
        required=True,
    )


class CapacitySecurityPortsEditorForm(EditorForm):
    port_number = forms.IntegerField(
        label="Port Number",
        widget=forms.NumberInput(
            attrs={
                "class": "w-auto form-control",
            }
        ),
        required=True,
    )


class CapacityLocalityEditorForm(LocalityEditorForm):
    pass

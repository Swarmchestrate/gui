from django import forms

from editor.forms import (
    EditorForm,
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


# Cloud & Edge Capacity forms
class CapacityPriceEditorForm(EditorForm):
    instance_type = forms.CharField(
        label='Instance Type',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

    credits_per_hour = forms.IntegerField(
        label='Cost (Credits per Hour)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


class CapacityEnergyConsumptionEditorForm(EditorForm):
    type = forms.CharField(
        label='Type',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

    amount = forms.CharField(
        label='Energy Consumed',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


class CapacitySecurityPortsEditorForm(EditorForm):
    port_number = forms.IntegerField(
        label='Port Number',
        widget=forms.NumberInput(attrs={
            'class': 'w-auto form-control',
        }),
        required=True
    )


# Cloud Capacity forms
class CloudCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class CloudCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'


class CloudCapacityArchitectureEditorForm(EditorForm):
    architecture_name = forms.CharField(
        label='Architecture Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


class CloudCapacityOperatingSystemEditorForm(EditorForm):
    os_name = forms.CharField(
        label='OS Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

    os_id = forms.CharField(
        label='OS Identifier',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


# Edge Capacity forms
class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class EdgeCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'


class EdgeCapacityAccessibleSensorsEditorForm(EditorForm):
    sensor_name = forms.CharField(
        label='Sensor Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


class EdgeCapacityDevicesEditorForm(EditorForm):
    device_type = forms.ChoiceField(
        label='Device Type',
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        choices=[
            ('', ''),
            ('hardware', 'Hardware'),
            ('software', 'Software'),
        ],
        required=True
    )

    device_name = forms.CharField(
        label='Device Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

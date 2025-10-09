from django import forms

from .dataclasses import GpsLocation

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

    credits_per_hour = forms.FloatField(
        label='Cost (Credits per Hour)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.0001',
        }),
        required=True
    )


class CapacityEnergyConsumptionEditorForm(EditorForm):
    type = forms.CharField(
        label='Type',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='E.g. CPU-based',
        required=True
    )

    amount = forms.CharField(
        label='Energy Consumed',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='E.g. 5W',
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


class CapacityLocalityEditorForm(EditorForm):
    continent = forms.CharField(
        label='Continent',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='e.g. Europe',
        required=False
    )

    country = forms.CharField(
        label='Country',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='e.g. United Kingdom',
        required=False
    )

    city = forms.CharField(
        label='City',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='e.g. London',
        required=False
    )

    gps = forms.CharField(
        label='GPS Location',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        help_text='e.g. 51.5072, -0.1276',
        required=False
    )


class CapacityLocalityOptionsSearchForm(forms.Form):
    query = forms.CharField(
        label='Search by Location Name',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': "e.g. 'Mauritius' or 'London'",
        }),
        help_text='Enter the name of a continent, country or city.',
        required=False
    )


class CapacityGetLocalityByNameForm(forms.Form):
    geoname_id = forms.IntegerField(
        required=True
    )

    continent_code = forms.CharField(
        required=False
    )

    country_code = forms.CharField(
        required=False
    )

    city_name = forms.CharField(
        required=False
    )


class SplitGpsLocationWidget(forms.MultiWidget):
    template_name = 'capacities/field_templates/gps_location_widget.html'

    def decompress(self, value):
        if value:
            return [value.get('latitude'), value.get('longitude')]
        return [None, None]


class GpsLocationField(forms.MultiValueField):
    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter both latitude and longitude.',
        }
        # Fields
        fields = (
            forms.FloatField(
                error_messages={'incomplete': 'Enter the latitude'},
                label='Latitude',
                required=True
            ),
            forms.FloatField(
                error_messages={'incomplete': 'Enter the longitude'},
                label='Longitude',
                required=True
            ),
        )
        super().__init__(
            error_messages=error_messages,
            fields=fields,
            require_all_fields=True,
            **kwargs
        )

    def compress(self, data_list):
        if not data_list:
            return GpsLocation(
                latitude=None,
                longitude=None
            )
        return GpsLocation(
            latitude=data_list[0],
            longitude=data_list[1]
        )


class CapacityGetLocalityByGpsForm(forms.Form):
    gps_location = GpsLocationField(
        label='Search by GPS Location',
        widget=SplitGpsLocationWidget(widgets={
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 51.5072',
                'step': 'any',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. -0.1276',
                'step': 'any',
            }),
        }),
        help_text='Enter the GPS co-ordinates of an edge device. e.g. 51.5072, -0.1276',
        required=False
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

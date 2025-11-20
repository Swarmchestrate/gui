from django import forms

from editor.forms.base_forms import EditorForm


class LocalityEditorForm(EditorForm):
    form_prefix = forms.CharField(widget=forms.HiddenInput(), required=False)

    continent = forms.CharField(
        label="Continent",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. Europe",
        required=False,
    )

    country = forms.CharField(
        label="Country",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. United Kingdom",
        required=False,
    )

    city = forms.CharField(
        label="City",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. London",
        required=False,
    )

    gps = forms.CharField(
        label="GPS Location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. 51.5072, -0.1276",
        required=False,
    )


class LocalityOptionsSearchForm(forms.Form):
    query = forms.CharField(
        label="Enter a Continent/Country/City Name",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "e.g. 'Mauritius' or 'London'",
            }
        ),
        help_text="Enter the name of a continent, country or city.",
        required=False,
    )


class GetLocalityByNameForm(forms.Form):
    geoname_id = forms.IntegerField(required=True)

    continent_code = forms.CharField(required=False)

    country_code = forms.CharField(required=False)

    city_name = forms.CharField(required=False)


class SplitGpsLocationWidget(forms.MultiWidget):
    template_name = "capacities/field_templates/gps_location_widget.html"

    def decompress(self, value):
        if value:
            return [value.get("latitude"), value.get("longitude")]
        return [None, None]


class GpsLocationField(forms.MultiValueField):
    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            "incomplete": "Enter both latitude and longitude.",
        }
        # Fields
        fields = (
            forms.FloatField(
                error_messages={"incomplete": "Enter the latitude"},
                label="Latitude",
                required=True,
            ),
            forms.FloatField(
                error_messages={"incomplete": "Enter the longitude"},
                label="Longitude",
                required=True,
            ),
        )
        super().__init__(
            error_messages=error_messages,
            fields=fields,
            require_all_fields=True,
            **kwargs,
        )

    def compress(self, data_list):
        if not data_list:
            return (None, None)
        return (data_list[0], data_list[1])


class GetLocalityByGpsForm(forms.Form):
    gps_location = GpsLocationField(
        label="Enter the Edge Device's GPS Co-ordinates",
        widget=SplitGpsLocationWidget(
            widgets={
                "latitude": forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "e.g. 51.5072",
                        "step": "any",
                        "min": -90,
                        "max": 90,
                    }
                ),
                "longitude": forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "e.g. -0.1276",
                        "step": "any",
                        "min": -180,
                        "max": 180,
                    }
                ),
            }
        ),
        help_text="Enter the GPS co-ordinates of an edge device. e.g. 51.5072 (-90 to 90), -0.1276 (-180 to 180)",
        required=False,
    )

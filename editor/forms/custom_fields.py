from django import forms


class EnumField(forms.ChoiceField):
    def clean(self, value):
        cleaned_data = super().clean(value)
        if not value:
            # Empty string is not accepted as
            # a null value in the database, so
            # change it to "None" instead.
            cleaned_data = None
        return cleaned_data


class GeometryPointField(forms.MultiValueField):
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
            return None
        return f"POINT({data_list[0]} {data_list[1]})"

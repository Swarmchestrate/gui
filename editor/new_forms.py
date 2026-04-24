from django import forms


class EditorForm(forms.Form):
    error_css_class = "is-invalid"
    
    def __init__(self, *args, **kwargs):
        if "initial" not in kwargs:
            super().__init__(*args, **kwargs)
        initial = kwargs["initial"]
        # Transform GPS location property value to something
        # easier to work with (if it exists).
        gps_location_property_name = "gps_location"
        gps_location = initial.get(gps_location_property_name)
        if gps_location:
            coordinates = gps_location.get("coordinates", [])
            lat, long = coordinates[0], coordinates[1]
            initial.update({gps_location_property_name: [lat, long]})
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        fields_with_errors = self.errors
        if "__all__" in self.errors:
            fields_with_errors = self.fields
        for field_name in fields_with_errors:
            try:
                field = self.fields[field_name]
                f_classes = field.widget.attrs.get("class", "").split(" ")
                f_classes.append(self.error_css_class)
                field.widget.attrs.update({"class": " ".join(f_classes)})
            except KeyError:
                continue
        return cleaned_data


class FormWithDynamicallyPopulatedFields(EditorForm):
    def __init__(self, *args, fields: dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        if not fields:
            fields = dict()
        for field_name, field in fields.items():
            self.fields.update({field_name: field})


class ForeignKeyFormWithDynamicallyPopulatedFields(FormWithDynamicallyPopulatedFields):
    def __init__(
            self,
            *args,
            fields: dict = None,
            id_prefix: str = "",
            id_suffix: str = "",
            **kwargs):
        auto_id = "id_%s"
        if id_prefix:
            auto_id = f"{id_prefix}-{auto_id}"
        if id_suffix:
            auto_id = f"{auto_id}-{id_suffix}"
        kwargs.update({"auto_id": auto_id})
        super().__init__(*args, fields=fields, **kwargs)

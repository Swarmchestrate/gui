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

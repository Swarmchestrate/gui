from django import forms

from editor.forms import (
    OpenApiSpecificationCategoryBasedForm,
    OpenApiSpecificationBasedRegistrationForm,
)


class CapacityPriceEditorForm(forms.Form):
    error_css_class = 'is-invalid'

    def is_valid(self):
        result = super().is_valid()
        fields_with_errors = self.errors
        if '__all__' in self.errors:
            fields_with_errors = self.fields
        for field_name in fields_with_errors:
            attrs = self.fields[field_name].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result

    price_instance_type = forms.CharField(
        label='Instance Type',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )

    price_credits_per_hour = forms.CharField(
        label='Credits',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=True
    )


class CloudCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class CloudCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'


class EdgeCapacityRegistrationForm(OpenApiSpecificationBasedRegistrationForm):
    definition_name = 'capacity'


class EdgeCapacityEditorForm(OpenApiSpecificationCategoryBasedForm):
    definition_name = 'capacity'

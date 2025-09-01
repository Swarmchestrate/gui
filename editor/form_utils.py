from django import forms


class DefaultConfiguredField:
    field_class = forms.CharField
    widget_class = forms.Textarea

    def __init__(
            self,
            field_properties: dict,
            is_required: bool = False) -> None:
        self.field_properties = field_properties
        self.is_required = is_required

    def get_widget_classes(self) -> list[str]:
        return ['form-control']

    def get_widget_kwargs(self) -> dict:
        return {
            'attrs': {
                'class': ' '.join(self.get_widget_classes()),
            }
        }

    def get_field_kwargs(self) -> dict:
        kwargs = {
            'required': self.is_required,
            'widget': self.widget_class(**self.get_widget_kwargs()),
        }
        field_description = self.field_properties.get('description')
        if not field_description:
            return kwargs
        kwargs.update({
            'help_text': field_description,
        })
        return kwargs

    @property
    def field_instance(self) -> forms.Field:
        return self.field_class(**self.get_field_kwargs())


class ConfiguredBooleanField(DefaultConfiguredField):
    field_class = forms.BooleanField
    widget_class = forms.CheckboxInput

    def get_widget_classes(self) -> list[str]:
        return ['form-check-input']


class ConfiguredCharField(DefaultConfiguredField):
    field_class = forms.CharField
    widget_class = forms.TextInput

    def get_field_kwargs(self) -> dict:
        kwargs = super().get_field_kwargs()
        max_length = self.field_properties.get('maxLength')
        if not max_length:
            return kwargs
        kwargs.update({
            'max_length': max_length,
        })
        return kwargs


class ConfiguredChoiceField(DefaultConfiguredField):
    field_class = forms.ChoiceField
    widget_class = forms.Select


class ConfiguredDateField(DefaultConfiguredField):
    field_class = forms.DateField
    widget_class = forms.DateInput


class ConfiguredIntegerField(DefaultConfiguredField):
    field_class = forms.IntegerField
    widget_class = forms.NumberInput


class ConfiguredMultipleChoiceField(DefaultConfiguredField):
    field_class = forms.MultipleChoiceField
    widget_class = forms.SelectMultiple


class ConfiguredTextField(DefaultConfiguredField):
    field_class = forms.CharField
    widget_class = forms.Textarea
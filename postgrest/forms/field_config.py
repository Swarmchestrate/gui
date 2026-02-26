from django import forms
from django.forms import Widget

from .custom_fields import EnumField, GeometryPointField
from .custom_widgets import (
    GeometryPointWidget,
    SelectWithDisabledFirstOption,
)
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY


class FieldConfig:
    # Overridden by child classes inheriting
    # from FieldConfig.
    field_class = forms.CharField
    css_classes = ['form-control']
    extra_field_kwargs = dict()
    extra_widget_kwargs = dict()
    extra_widget_attrs = dict()

    def __init__(
            self,
            field_name: str,
            is_required: bool = False,
            label: str | None = None,
            help_text: str | None = None,
            category: str | None = None):
        self.field_name = field_name
        self.is_required = is_required
        self.label = label
        self.help_text = help_text
        self.category = category

    @property
    def widget_class(self) -> Widget:
        return self.field_class.widget
    
    # Field methods
    def _setup_field_kwargs(self) -> dict:
        kwargs = {
            "required": self.is_required,
            "widget": self.widget_class(
                attrs={
                    "class": " ".join(self.css_classes),
                    **self.extra_widget_attrs
                },
                **self.extra_widget_kwargs,
            ),
        }
        kwargs.update({
            "label": self.label,
        })
        if self.help_text:
            kwargs.update({
                "help_text": self.help_text,
            })
            kwargs["widget"].attrs.update({
                "aria-describedby": f"{self.field_name}-help-text",
            })
        kwargs.update(self.extra_field_kwargs)
        return kwargs
    
    def get_field(self):
        field_kwargs = self._setup_field_kwargs()
        field = self.field_class(**field_kwargs)
        field.category = UNKNOWN_ATTRIBUTE_CATEGORY
        if self.category:
            field.category = self.category
        return field


class DefaultFieldConfig(FieldConfig):
    pass


class BooleanFieldConfig(FieldConfig):
    field_class = forms.BooleanField
    css_classes = ["form-check-input"]


class ChoiceFieldConfig(FieldConfig):
    CHOICES_NOT_SPECIFIED = "Choices have not been specified."
    
    def __init__(self, choices: list[tuple[str, str]], *args, **kwargs):
        if not choices:
            raise Exception(self.CHOICES_NOT_SPECIFIED)
        super().__init__(*args, **kwargs)
        self.extra_field_kwargs = {
            "choices": choices,
        }

    field_class = EnumField
    widget_class = SelectWithDisabledFirstOption
    css_classes = ["form-select"]


class DateFieldConfig(FieldConfig):
    field_class = forms.DateField


class IntegerFieldConfig(FieldConfig):
    field_class = forms.IntegerField
    extra_field_kwargs = {"min_value": 1, "step_size": 1}


class JsonFieldConfig(FieldConfig):
    widget_class = forms.Textarea


class NumericFieldConfig(FieldConfig):
    field_class = forms.FloatField
    extra_widget_attrs = {"step": "any"}


class GeometryPointFieldConfig(FieldConfig):
    field_class = GeometryPointField
    widget_class = GeometryPointWidget
    extra_widget_kwargs = {
        "widgets": {
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
    }
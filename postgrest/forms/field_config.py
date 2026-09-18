from django import forms
from django.forms import Widget

from .custom_fields import EnumField, GeometryPointField
from .custom_widgets import (
    CheckboxListWidget,
    GeometryPointWidget,
    KeyValueWidget,
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
            metadata: dict,
            is_required: bool = False,
            label: str | None = None,
            help_text: str | None = None,
            category: str | None = None):
        self.field_name = field_name
        self.metadata = metadata
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
        field.metadata = self.metadata
        return field


class DefaultFieldConfig(FieldConfig):
    pass


class BooleanFieldConfig(FieldConfig):
    field_class = forms.BooleanField
    css_classes = ["form-check-input"]

    def _setup_field_kwargs(self) -> dict:
        kwargs = super()._setup_field_kwargs()
        # A required BooleanField in Django means "must be ticked", but a
        # non-null boolean column only means "must have a value" - and an
        # unchecked box already submits a valid False.
        kwargs["required"] = False
        return kwargs


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


class MultipleChoiceFieldConfig(FieldConfig):
    """A list column whose entries must each be one of known choices.

    Checkboxes, because the choices are few and all of them should be visible -
    the microservices a reconfiguration policy may target, for instance.
    """

    def __init__(self, choices: list[tuple[str, str]], *args, **kwargs):
        if not choices:
            raise Exception(ChoiceFieldConfig.CHOICES_NOT_SPECIFIED)
        super().__init__(*args, **kwargs)
        self.extra_field_kwargs = {"choices": choices}

    field_class = forms.MultipleChoiceField
    widget_class = CheckboxListWidget
    css_classes = []


class KeyValueFieldConfig(FieldConfig):
    """A jsonb column holding a flat map of names to values."""

    field_class = forms.JSONField
    widget_class = KeyValueWidget
    css_classes = []


class TextareaFieldConfig(FieldConfig):
    """Text too long for a single line, such as a reconfiguration rule."""

    widget_class = forms.Textarea
    css_classes = ["form-control", "font-monospace"]
    extra_widget_attrs = {"rows": 16, "spellcheck": "false"}
    # Kept exactly as typed: a rule's leading indentation and final newline are
    # part of what the user wrote.
    extra_field_kwargs = {"strip": False}


class DateFieldConfig(FieldConfig):
    field_class = forms.DateField


class IntegerFieldConfig(FieldConfig):
    field_class = forms.IntegerField
    extra_field_kwargs = {"min_value": 1, "step_size": 1}


class JsonFieldConfig(FieldConfig):
    # Parses the text as JSON, so a jsonb column receives an object rather than
    # the typed characters as a JSON string.
    field_class = forms.JSONField
    widget_class = forms.Textarea
    extra_widget_attrs = {
        "autocomplete": "off",
    }


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


class TextArrayFieldConfig(FieldConfig):
    field_class = forms.JSONField
    widget_class = forms.HiddenInput
    extra_widget_attrs = {
        "data-type": "text[]",
    }
from enum import Enum

from django import forms

from .form_utils import (
    DefaultConfiguredField,
    ConfiguredBooleanField,
    ConfiguredCharField,
    ConfiguredDateField,
    ConfiguredFloatField,
    ConfiguredIntegerField,
    ConfiguredJsonField,
    ConfiguredTextField,
)

from editor.api_endpoint_client import ApiEndpointClient


class OpenApiPropertyFormat(Enum):
    BOOLEAN = 'boolean'
    CHARACTER_VARYING = 'character varying'
    DATE = 'timestamp without time zone'
    INTEGER = 'integer'
    JSONB = 'jsonb'
    NUMERIC = 'numeric'
    TEXT = 'text'
    TEXT_ARRAY = 'text[]'


class OpenApiSpecificationBasedForm(forms.Form):
    error_css_class = 'is-invalid'
    definition_name = ''

    def __init__(self, api_endpoint_client: ApiEndpointClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_endpoint_client = api_endpoint_client
        field_data = self.get_data_for_form_fields()
        required_field_names = self.api_endpoint_client.endpoint_definition.get_required_user_specifiable_fields()
        self.populate_form_fields(field_data, required_field_names)

    def is_valid(self):
        is_valid = super().is_valid()
        errors = self.errors.as_data()
        for field_name in errors:
            try:
                field = self.fields[field_name]
                f_classes = field.widget.attrs.get('class', '').split(' ')
                f_classes.append(self.error_css_class)
                field.widget.attrs.update({
                    'class': ' '.join(f_classes),
                })
            except KeyError:
                continue
        return is_valid

    def get_data_for_form_fields(self):
        return self.api_endpoint_client.endpoint_definition.get_all_user_specifiable_fields()

    def populate_form_fields(self, field_data: dict, required_field_names: list):
        for field_key, field_metadata in field_data.items():
            is_required = field_key in required_field_names
            new_field = self._get_configured_field(field_metadata, is_required=is_required)
            self.fields.update({
                field_key: new_field,
            })

    def _get_configured_field_class(self, field_format: str):
        match field_format:
            case OpenApiPropertyFormat.BOOLEAN:
                return ConfiguredBooleanField
            case OpenApiPropertyFormat.CHARACTER_VARYING:
                return ConfiguredCharField
            case OpenApiPropertyFormat.DATE:
                return ConfiguredDateField
            case OpenApiPropertyFormat.INTEGER:
                return ConfiguredIntegerField
            case OpenApiPropertyFormat.JSONB:
                return ConfiguredJsonField
            case OpenApiPropertyFormat.NUMERIC:
                return ConfiguredFloatField
            case OpenApiPropertyFormat.TEXT:
                return ConfiguredTextField
            case OpenApiPropertyFormat.TEXT_ARRAY:
                return ConfiguredTextField
            case _:
                return DefaultConfiguredField

    def _get_configured_field(self, field_metadata: dict, is_required: bool = False):
        field_format = field_metadata.get('format')
        try:
            field_format = OpenApiPropertyFormat(field_format)
        except ValueError:
            pass
        configured_field_kwargs = {
            'is_required': is_required,
        }
        configured_field_class = self._get_configured_field_class(field_format)
        return configured_field_class(
            field_metadata,
            **configured_field_kwargs
        ).field_instance


class OpenApiSpecificationFieldFormatBasedForm(OpenApiSpecificationBasedForm):
    def __init__(self, api_endpoint_client: ApiEndpointClient, field_format: str, *args, **kwargs):
        self.field_format = field_format
        super().__init__(api_endpoint_client, *args, **kwargs)

    def get_data_for_form_fields(self):
        return self.api_endpoint_client.endpoint_definition.get_user_specifiable_fields_with_format(self.field_format)


class OpenApiSpecificationBasedRegistrationForm(OpenApiSpecificationBasedForm):
    def get_data_for_form_fields(self):
        return self.api_endpoint_client.endpoint_definition.get_required_user_specifiable_fields()
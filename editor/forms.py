from enum import Enum

from django import forms

from .form_utils import (
    DefaultConfiguredField,
    ConfiguredBooleanField,
    ConfiguredCharField,
    ConfiguredDateField,
    ConfiguredIntegerField,
    ConfiguredTextField,
)

from editor.api_client import ApiClient


class OpenApiFormat(Enum):
    BOOLEAN = 'boolean'
    CHARACTER_VARYING = 'character varying'
    DATE = 'timestamp without time zone'
    INTEGER = 'integer'
    TEXT = 'text'
    TEXT_ARRAY = 'text[]'


class OpenApiSpecificationBasedForm(forms.Form):
    definition_name = ''

    def __init__(self, api_client: ApiClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_client = api_client
        field_data = self.get_data_for_form_fields()
        required_field_names = self.api_client.get_required_field_names()
        self.populate_form_fields(field_data, required_field_names)

    def get_data_for_form_fields(self):
        return self.api_client.get_all_fields()

    def populate_form_fields(self, field_data: dict, required_field_names: list):
        for field_key, field_metadata in field_data.items():
            is_required = field_key in required_field_names
            new_field = self._get_configured_field(field_metadata, is_required=is_required)
            self.fields.update({
                field_key: new_field,
            })

    def _get_configured_field(self, field_metadata: dict, is_required: bool = False):
        field_format = field_metadata.get('format')
        try:
            field_format = OpenApiFormat(field_format)
        except ValueError:
            pass
        match field_format:
            case OpenApiFormat.BOOLEAN:
                return ConfiguredBooleanField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.CHARACTER_VARYING:
                return ConfiguredCharField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.DATE:
                return ConfiguredDateField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.INTEGER:
                return ConfiguredIntegerField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.TEXT:
                return ConfiguredCharField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.TEXT_ARRAY:
                return ConfiguredTextField(field_metadata, is_required=is_required).field_instance
            case _:
                return DefaultConfiguredField(field_metadata, is_required=is_required).field_instance


class OpenApiSpecificationFieldFormatBasedForm(OpenApiSpecificationBasedForm):
    def __init__(self, api_client: ApiClient, field_format: str, *args, **kwargs):
        self.field_format = field_format
        super().__init__(api_client, *args, **kwargs)

    def get_data_for_form_fields(self):
        return self.api_client.get_fields_with_format(self.field_format)
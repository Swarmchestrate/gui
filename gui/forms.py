import os
from django import forms
from django.conf import settings
from enum import Enum
from prance import ResolvingParser

from .form_utils import (
    DefaultConfiguredField,
    ConfiguredBooleanField,
    ConfiguredCharField,
    ConfiguredDateField,
    ConfiguredIntegerField,
)


CAPACITY_PATH = '/model'


class OpenApiFormat(Enum):
    BOOLEAN = 'boolean'
    CHARACTER_VARYING = 'character varying'
    DATE = 'date'
    INTEGER = 'integer'
    UUID = 'uuid'


class NewCapacityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parser = ResolvingParser(os.path.join(settings.BASE_DIR, 'swagger.yaml'))
        post_parameters_schema = next(iter(parser.specification.get('paths').get(CAPACITY_PATH).get('post').get('parameters'))).get('schema')
        required_field_names = post_parameters_schema.get('required')
        fields = post_parameters_schema.get('properties')
        for field_key, field_metadata in fields.items():
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
            case OpenApiFormat.CHARACTER_VARYING | OpenApiFormat.UUID:
                return ConfiguredCharField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.DATE:
                return ConfiguredDateField(field_metadata, is_required=is_required).field_instance
            case OpenApiFormat.INTEGER:
                return ConfiguredIntegerField(field_metadata, is_required=is_required).field_instance
            case _:
                return DefaultConfiguredField(field_metadata, is_required=is_required).field_instance
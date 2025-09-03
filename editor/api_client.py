import os
import requests
from prance import ResolvingParser

from django.conf import settings


class ApiClient:
    def __init__(self) -> None:
        self.definition_name = None
        self.endpoint = None
        self.id_field = None
        self.api_url = os.environ.get('API_URL')
        self.openapi_spec_url = os.environ.get('OPENAPI_SPEC_URL')

    @property
    def endpoint_url(self):
        return f'{self.api_url}/{self.endpoint}'

    def _get_definition(self):
        openapi_spec = self.get_openapi_spec()
        return (openapi_spec
                .get('definitions', {})
                .get(self.definition_name, {}))


    def get_openapi_spec(self):
        # TEMP - API spec currently not parsing correctly
        parser = ResolvingParser(os.path.join(settings.BASE_DIR, 'swagger.yaml'))
        return parser.specification
        # response = requests.get(self.api_url)
        # response.raise_for_status()
        # return response.json()

    # Registrations
    def get_registrations(self, params: dict = dict()):
        response = requests.get(
            self.endpoint_url,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def register(self, data: dict):
        print('data', data)
        response = requests.post(self.endpoint_url, data=data)
        response.raise_for_status()

    def delete(self, registration_id: int, params: dict = dict()):
        params.update({
            self.id_field: f'eq.{registration_id}',
        })
        response = requests.delete(self.endpoint_url, params=params)
        response.raise_for_status()

    # Utils
    def get_required_field_names(self):
        return self._get_definition().get('required', list())

    def get_field_formats(self):
        definition_properties = self._get_definition().get('properties', {})
        return list(set(
            value.get('format')
            for value in definition_properties.values()
        ))

    # Fields
    def get_all_fields(self):
        return self._get_definition().get('properties', {})

    def get_fields_with_format(self, format: str):
        definition_properties = self._get_definition().get('properties', {})
        return {
            key: value
            for key, value in definition_properties.items()
            if value.get('format') == format
        }

    def get_fields_with_names(self, names: list[str]):
        definition_properties = self._get_definition().get('properties', {})
        return {
            key: value
            for key, value in definition_properties.items()
            if key in names
        }

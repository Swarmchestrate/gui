import os
import random
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
        self.random_id_min_value = 0
        self.random_id_max_value = 999999

    @property
    def endpoint_url(self):
        return f'{self.api_url}/{self.endpoint}'

    # Helpers
    def _get_existing_registration_ids(self):
        params = {
            'select': f'{self.id_field}'
        }
        return [
            data.get(self.id_field)
            for data in self.get_registrations(params=params)
        ]

    def _get_all_fields(self) -> dict:
        return self._get_definition().get('properties', {})

    def _get_fields_with_names(self, names: list[str]):
        all_fields = self._get_all_fields()
        return {
            key: value
            for key, value in all_fields.items()
            if key in names
        }

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
    def get(self, registration_id: int):
        response = requests.get(
            self.endpoint_url,
            params={
                self.id_field: registration_id,
            }
        )
        response.raise_for_status()
        return response.json()

    def get_registrations(self, params: dict = dict()):
        response = requests.get(
            self.endpoint_url,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def register(self, data: dict):
        response = requests.post(self.endpoint_url, json=data)
        response.raise_for_status()

    def delete(self, registration_id: int, params: dict = dict()):
        params.update({
            self.id_field: f'eq.{registration_id}',
        })
        response = requests.delete(self.endpoint_url, params=params)
        response.raise_for_status()

    # Utils
    def _generate_random_id(self):
        existing_registration_ids = self._get_existing_registration_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(range(
            self.random_id_min_value,
            self.random_id_max_value
        ))
        existing_ids_set = set(existing_registration_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        random_id = random.choice(list(possible_ids_set))
        return random_id

    def get_required_field_names(self):
        return self._get_definition().get('required', list())

    def get_required_field_names_specified_by_user(self):
        required_field_names = set(self.get_required_field_names())
        auto_generated_field_names = set(self.auto_generated_field_names())
        return list(required_field_names - auto_generated_field_names)

    def auto_generated_field_names(self):
        return list([self.id_field])

    def get_field_formats(self):
        definition_properties = self._get_definition().get('properties', {})
        return list(set(
            value.get('format')
            for value in definition_properties.values()
        ))

    # Fields
    def get_all_fields(self):
        return self._get_all_fields()

    def get_fields_with_format(self, format: str):
        all_fields = self._get_all_fields()
        return {
            key: value
            for key, value in all_fields.items()
            if value.get('format') == format
        }

    def get_required_fields(self):
        field_names = self.get_required_field_names()
        return self._get_fields_with_names(field_names)

    def get_required_fields_specified_by_user(self):
        field_names = self.get_required_field_names_specified_by_user()
        return self._get_fields_with_names(field_names)

    def get_fields_with_names(self, names: list[str]):
        return self._get_fields_with_names(names)

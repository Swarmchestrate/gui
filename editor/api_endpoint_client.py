import os
import random
import requests

from .api_client import ApiClient
from .definitions import UserSpecifiableOpenApiDefinition


class ApiEndpointClient(ApiClient):
    endpoint: str
    endpoint_definition: UserSpecifiableOpenApiDefinition
    endpoint_definition_class: UserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        super().__init__()
        openapi_spec = self.get_openapi_spec()
        self.endpoint_definition = self.endpoint_definition_class(openapi_spec)
        self.openapi_spec_url = os.environ.get('OPENAPI_SPEC_URL')
        self.random_id_min_value = 0
        self.random_id_max_value = 999999

    @property
    def endpoint_url(self):
        return f'{self.api_url}/{self.endpoint}'

    # Helpers
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

    def _get_existing_registration_ids(self):
        params = {
            'select': f'{self.endpoint_definition.id_field}'
        }
        return [
            data.get(self.endpoint_definition.id_field)
            for data in self.get_registrations(params=params)
        ]

    # Registrations
    def get(self, registration_id: int):
        response = requests.get(
            self.endpoint_url,
            params={
                self.endpoint_definition.id_field: registration_id,
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
        data.update({
            self.endpoint_definition.id_field: self._generate_random_id(),
        })
        response = requests.post(self.endpoint_url, json=data)
        response.raise_for_status()

    def delete(self, registration_id: int, params: dict = dict()):
        params.update({
            self.endpoint_definition.id_field: f'eq.{registration_id}',
        })
        response = requests.delete(self.endpoint_url, params=params)
        response.raise_for_status()
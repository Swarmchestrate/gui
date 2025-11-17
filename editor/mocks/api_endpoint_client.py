import json
import logging
import os
import random
import shutil
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings

from .api_client import TestApiClient
from ..abc import BaseApiEndpointClient
from ..definitions import (
    ColumnMetadataUserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinition,
)


logger = logging.getLogger(__name__)


class TestApiEndpointClient(BaseApiEndpointClient, TestApiClient):
    endpoint: str
    endpoint_definition: UserSpecifiableOpenApiDefinition
    endpoint_definition_class: UserSpecifiableOpenApiDefinition

    path_to_data: os.PathLike | str
    path_to_temp_data_dir: os.PathLike | str

    def __init__(self) -> None:
        super().__init__()
        openapi_spec = self.get_openapi_spec()
        self.endpoint_definition = self.endpoint_definition_class(openapi_spec)
        self.random_id_min_value = 0
        self.random_id_max_value = 999999
        path_to_data_basename = os.path.basename(self.path_to_data)
        self.path_to_temp_data = os.path.join(self.path_to_temp_data_dir, path_to_data_basename)

    # Helpers
    def _get_existing_registration_ids(self):
        params = {
            'select': f'{self.endpoint_definition.id_field}'
        }
        return [
            data.get(self.endpoint_definition.id_field)
            for data in self.get_registrations(params=params)
        ]

    def _generate_random_id(self):
        existing_registration_ids = self._get_existing_registration_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(range(
            self.random_id_min_value,
            self.random_id_max_value
        ))
        existing_ids_set = set(existing_registration_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error('There are no new unique IDs that can be used.')
        random_id = random.choice(possible_ids_set)
        return random_id

    def _generate_random_ids(self, amount: int = 1):
        existing_registration_ids = self._get_existing_registration_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(range(
            self.random_id_min_value,
            self.random_id_max_value
        ))
        existing_ids_set = set(existing_registration_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error('There are no new unique IDs that can be used.')
        random_ids = random.sample(list(possible_ids_set), int(amount))
        if len(random_ids) != amount:
            raise Error(f'Failed to generate {amount} new unique IDs.')
        return random_ids

    def _create_temp_data_if_not_exists(self):
        Path(self.path_to_temp_data_dir).mkdir(parents=True, exist_ok=True)
        data_file_basename = os.path.basename(self.path_to_data)
        temp_data_file = Path(self.path_to_temp_data)
        if temp_data_file.is_file():
            return
        shutil.copyfile(
            self.path_to_data,
            self.path_to_temp_data
        )

    def _get_temp_data_and_create_if_not_exists(self):
        self._create_temp_data_if_not_exists()
        temp_data = None
        with open(self.path_to_temp_data, 'r') as f:
            temp_data = json.loads(f.read())
        return temp_data

    def _update_temp_data(self, update_data: list):
        with open(self.path_to_temp_data, 'w') as f:
            f.write(
                json.dumps(update_data, indent=4)
            )

    # Registrations
    def get(self, registration_id: int, params: dict = None) -> dict:
        registrations = self._get_temp_data_and_create_if_not_exists()
        registration = {}
        for r in registrations:
            r_id = r.get(self.endpoint_definition.id_field)
            if not r_id:
                continue
            if not int(r_id) == int(registration_id):
                continue
            registration = r
            break
        return registration

    def get_registrations_by_ids(self, registration_ids: list[int], params: dict | None = None) -> list[dict]:
        all_registrations = self._get_temp_data_and_create_if_not_exists()
        registrations = [
            r for r in all_registrations
            if int(r.get(self.endpoint_definition.id_field)) in registration_ids
        ]
        return registrations

    def get_registrations(self, params: dict = None):
        registrations = self._get_temp_data_and_create_if_not_exists()
        return registrations

    def register(self, data: dict) -> dict:
        registrations = self._get_temp_data_and_create_if_not_exists()
        new_id = self._generate_random_id()
        data.update({
            self.endpoint_definition.id_field: new_id,
        })
        if any(
            int(r.get(self.endpoint_definition.id_field)) == int(new_id)
            for r in registrations
        ):
            return {}
        registrations.append(data)
        self._update_temp_data(registrations)
        return data

    def bulk_register(self, data_list: list[dict]) -> list[int]:
        registrations = self._get_temp_data_and_create_if_not_exists()
        new_ids = self._generate_random_ids(amount=len(data_list))
        try:
            for i, data in enumerate(data_list):
                data.update({
                    self.endpoint_definition.id_field: new_ids[i]
                })
        except IndexError:
            raise Error('An error occurred whilst assigning IDs for bulk registration.')
        updated_registrations = registrations + data_list
        self._update_temp_data(updated_registrations)
        return new_ids

    def delete(self, registration_id: int, params: dict = None):
        registrations = self._get_temp_data_and_create_if_not_exists()
        updated_registrations = [
            r for r in registrations
            if not (
                int(r.get(self.endpoint_definition.id_field)) == int(registration_id)
            )
        ]
        return self._update_temp_data(updated_registrations)

    def delete_many(self, registration_ids: list[int]):
        registrations = self._get_temp_data_and_create_if_not_exists()
        updated_registrations = [
            r for r in registrations
            if not (
                int(r.get(self.endpoint_definition.id_field)) in registration_ids
            )
        ]
        return self._update_temp_data(updated_registrations)

    def _prepare_update_data(self, data: dict) -> dict:
        current_time = datetime.now(timezone.utc).isoformat()
        current_time_no_tz = str(current_time).replace('+00:00', '')
        data.update({
            'updated_at': current_time_no_tz,
        })
        return data

    def update(self, registration_id: int, data: dict):
        registration_to_update = self.get(registration_id)
        prepared_update_data = self._prepare_update_data(data)
        registration_to_update.update(prepared_update_data)
        registrations = self._get_temp_data_and_create_if_not_exists()
        updated_registrations = [
            r for r in registrations
            if not (
                int(r.get(self.endpoint_definition.id_field)) == int(registration_id)
            )
        ]
        updated_registrations.append(registration_to_update)
        return self._update_temp_data(updated_registrations)


class TestColumnMetadataApiEndpointClient(TestApiEndpointClient):
    path_to_data = os.path.join(settings.BASE_DIR, 'editor', 'mocks', 'column_metadata.json')
    path_to_temp_data_dir = os.path.join(settings.BASE_DIR, 'editor', 'temp')

    endpoint_definition_class = ColumnMetadataUserSpecifiableOpenApiDefinition

    def get_by_category(self, category: str):
        registrations = self.get_registrations()
        return [
            r
            for r in registrations
            if r.get('category') == category
        ]

    def get_by_table_name(self, table_name: str):
        registrations = self.get_registrations()
        return [
            r
            for r in registrations
            if r.get('table_name') == table_name
        ]

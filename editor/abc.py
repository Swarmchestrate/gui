import random
from abc import ABC, abstractmethod
from typing import Type

import requests


class BaseOpenApiDefinition:
    id_field: str

    # Properties
    @property
    def description(self) -> str:
        return self._get_definition().get("description", "")

    # Non-public methods
    @abstractmethod
    def _get_definition(self) -> dict:
        pass

    def _get_required_field_names(self):
        return self._get_definition().get("required", list())

    def _get_all_fields(self) -> dict:
        return self._get_definition().get("properties", {})

    def _get_fields_with_names(self, names: list[str]):
        all_fields = self._get_all_fields()
        return {key: value for key, value in all_fields.items() if key in names}


class BaseApiEndpointClient(ABC):
    endpoint_definition: BaseOpenApiDefinition
    endpoint_definition_class: Type[BaseOpenApiDefinition]

    random_id_min_value: int = 0
    random_id_max_value: int = 999999

    def log_and_raise_response_status_if_error(self, response: requests.Response):
        pass

    @abstractmethod
    def get_openapi_spec(self):
        pass

    @abstractmethod
    def _prepare_update_data(self, data: dict) -> dict:
        pass

    @abstractmethod
    def get(self, registration_id: int, params: dict | None = None) -> dict:
        pass

    @abstractmethod
    def get_registrations_by_ids(
        self, registration_ids: list[int], params: dict | None = None
    ) -> list[dict]:
        pass

    @abstractmethod
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        pass

    @abstractmethod
    def register(self, data: dict) -> dict:
        pass

    @abstractmethod
    def bulk_register(self, data_list: list[dict]) -> list[int]:
        pass

    @abstractmethod
    def update(self, registration_id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, registration_id: int, params: dict | None = None):
        pass

    @abstractmethod
    def delete_many(self, registration_ids: list[int]):
        pass

    def _get_existing_registration_ids(self):
        params = {"select": f"{self.endpoint_definition.id_field}"}
        return [
            data.get(self.endpoint_definition.id_field)
            for data in self.get_registrations(params=params)
        ]

    def _generate_random_id(self):
        existing_registration_ids = self._get_existing_registration_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_registration_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error("There are no new unique IDs that can be used.")
        random_id = random.choice(possible_ids_set)
        return random_id

    def _generate_random_ids(self, amount: int = 1):
        existing_registration_ids = self._get_existing_registration_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_registration_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error("There are no new unique IDs that can be used.")
        random_ids = random.sample(list(possible_ids_set), int(amount))
        if len(random_ids) != amount:
            raise Error(f"Failed to generate {amount} new unique IDs.")
        return random_ids

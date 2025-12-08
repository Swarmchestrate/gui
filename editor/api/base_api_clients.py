import json
import logging
import os
import random
from abc import ABC, abstractmethod
from ast import literal_eval as make_tuple
from datetime import datetime, timezone
from typing import Type

import requests

from .base_definitions import (
    BaseOpenApiDefinition,
    ColumnMetadataUserSpecifiableOpenApiDefinition,
)

logger = logging.getLogger(__name__)


# PostgREST API client
class BaseApiClientMixin(ABC):
    def log_and_raise_response_status_if_error(self, response: requests.Response):
        pass

    @abstractmethod
    def get_openapi_spec(self) -> dict:
        pass

    def get_definitions(self) -> dict:
        openapi_spec = self.get_openapi_spec()
        return openapi_spec.get("definitions", list())


class ApiClientMixin(BaseApiClientMixin):
    api_url: str

    def __init__(self):
        self.api_url = os.environ.get("API_URL", "")

    def get_openapi_spec(self) -> dict:
        response = requests.get(self.api_url)
        self.log_and_raise_response_status_if_error(response)
        return response.json()

    # Error handling
    def log_and_raise_response_status_if_error(self, response: requests.Response):
        if response.ok:
            return
        try:
            logger.error(json.dumps(response.json(), indent=2))
        except Exception:
            logger.exception("Could not log error response.")
        response.raise_for_status()


# PostgReST API client for an endpoint
class BaseApiClient(BaseApiClientMixin, ABC):
    endpoint: str
    endpoint_definition: BaseOpenApiDefinition
    endpoint_definition_class: Type[BaseOpenApiDefinition]

    random_id_min_value: int = 0
    random_id_max_value: int = 999999

    @classmethod
    def get_client_instance_by_endpoint(cls, endpoint_name: str) -> "BaseApiClient":
        client_instance = None
        for subclass in cls.__subclasses__():
            if not subclass.endpoint == endpoint_name:
                continue
            client_instance = subclass()
        return client_instance

    @abstractmethod
    def _prepare_update_data(self, data: dict) -> dict:
        pass

    @abstractmethod
    def get(self, resource_id: int, params: dict | None = None) -> dict:
        pass

    @abstractmethod
    def get_resources_by_ids(
        self, resource_ids: list[int], params: dict | None = None
    ) -> list[dict]:
        pass

    @abstractmethod
    def get_resources(self, params: dict | None = None) -> list[dict]:
        pass

    @abstractmethod
    def register(self, data: dict) -> dict:
        pass

    @abstractmethod
    def register_with_id(self, new_id: int, data: dict) -> dict:
        pass

    @abstractmethod
    def bulk_register(self, data_list: list[dict]) -> list[int]:
        pass

    @abstractmethod
    def update(self, resource_id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, resource_id: int, params: dict | None = None):
        pass

    @abstractmethod
    def delete_many(self, resource_ids: list[int]):
        pass

    # Helper methods
    def clean_data(self, uncleaned_data: dict) -> dict:
        uncleaned_data_copy = dict(uncleaned_data)
        definition_fields = self.endpoint_definition._get_all_fields().keys()
        for key in uncleaned_data.keys():
            if key in definition_fields:
                continue
            uncleaned_data_copy.pop(key)
        return uncleaned_data_copy

    def _get_existing_resource_ids(self):
        params = {"select": f"{self.endpoint_definition.id_field}"}
        return [
            data.get(self.endpoint_definition.id_field)
            for data in self.get_resources(params=params)
        ]

    def _generate_random_id(self):
        existing_resource_ids = self._get_existing_resource_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_resource_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error("There are no new unique IDs that can be used.")
        random_id = random.choice(list(possible_ids_set))
        return random_id

    def _generate_random_ids(self, amount: int = 1):
        existing_resource_ids = self._get_existing_resource_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_resource_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Error("There are no new unique IDs that can be used.")
        random_ids = random.sample(list(possible_ids_set), int(amount))
        if len(random_ids) != amount:
            raise Error(f"Failed to generate {amount} new unique IDs.")
        return random_ids


class ApiClient(ApiClientMixin, BaseApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    def __init__(self) -> None:
        super().__init__()
        openapi_spec = self.get_openapi_spec()
        self.endpoint_definition = self.endpoint_definition_class(openapi_spec)

    # Class properties
    @property
    def endpoint_url(self):
        return f"{self.api_url}/{self.endpoint}"

    # Resources
    def _get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return response.json()

    def get(self, resource_id: int, params: dict | None = None) -> dict:
        if not params:
            params = dict()
        params.update(
            {
                self.endpoint_definition.id_field: f"eq.{resource_id}",
            }
        )
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        # Responses are returned as lists, so need
        # to get the first list element.
        resource = next(iter(response.json()))
        return resource

    def get_resources_by_ids(self, resource_ids: list[int], params: dict | None = None):
        if not params:
            params = dict()
        params.update(
            {
                self.endpoint_definition.id_field: "in.(%s)"
                % ",".join([str(resource_id) for resource_id in resource_ids])
            }
        )
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return response.json()

    def get_resources(self, params: dict | None = None) -> list[dict]:
        return self._get_resources(params)

    def _register(self, new_id: int, data: dict) -> dict:
        cleaned_data = self.clean_data(data)
        cleaned_data.update(
            {
                self.endpoint_definition.id_field: new_id,
            }
        )
        response = requests.post(self.endpoint_url, json=cleaned_data)
        self.log_and_raise_response_status_if_error(response)
        new_resource = self.get(new_id)
        return new_resource

    def register(self, data: dict) -> dict:
        new_id = self._generate_random_id()
        return self._register(new_id, data)

    def register_with_id(self, new_id: int, data: dict) -> dict:
        return self._register(new_id, data)

    def bulk_register(self, data_list: list[dict]) -> list[int]:
        new_ids = self._generate_random_ids(amount=len(data_list))
        try:
            for i, data in enumerate(data_list):
                cleaned_data = self.clean_data(data)
                cleaned_data.update({self.endpoint_definition.id_field: new_ids[i]})
        except IndexError:
            raise Error("An error occurred whilst assigning IDs for bulk registration.")
        response = requests.post(self.endpoint_url, json=data_list)
        self.log_and_raise_response_status_if_error(response)
        return new_ids

    def delete(self, resource_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update(
            {
                self.endpoint_definition.id_field: f"eq.{resource_id}",
            }
        )
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)

    def delete_many(self, resource_ids: list[int]):
        params = {
            self.endpoint_definition.id_field: f"in.({','.join(map(str, resource_ids))})",
        }
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)

    def _prepare_update_data(self, data: dict):
        current_time = datetime.now(timezone.utc).isoformat()
        current_time_no_tz = str(current_time).replace("+00:00", "")
        data.update(
            {
                "updated_at": current_time_no_tz,
            }
        )
        return data

    def update(self, resource_id: int, data: dict):
        prepared_update_data = self._prepare_update_data(data)
        params = {
            self.endpoint_definition.id_field: f"eq.{resource_id}",
        }
        response = requests.patch(
            self.endpoint_url, params=params, json=prepared_update_data
        )
        self.log_and_raise_response_status_if_error(response)


# PostgREST API client for the column_metadata endpoint
class BaseColumnMetadataApiClient(BaseApiClient, ABC):
    endpoint = "column_metadata"
    disabled_categories: list[str] = list()


class ColumnMetadataApiClient(ApiClient, BaseColumnMetadataApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    endpoint_definition_class = ColumnMetadataUserSpecifiableOpenApiDefinition

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        if not self.disabled_categories:
            return self._get_resources(params)
        and_conditions = set(
            f"category.neq.{category}" for category in self.disabled_categories
        )
        if "and" in params:
            existing_and_conditions = make_tuple(params.get("and", "()"))
            for condition in existing_and_conditions:
                and_conditions.add(condition)
        if "category" in params:
            and_conditions.add(f"category.{params.get('category')}")
            params.pop("category", None)
        params.update(
            {
                "and": f"({','.join(and_conditions)})",
            }
        )
        return self._get_resources(params)

    def get_resources_by_category(self, category: str):
        return self.get_resources(params={"category": f"eq.{category}"})

    def get_by_table_name(self, table_name: str):
        return self.get_resources(params={"table_name": f"eq.{table_name}"})

    def get_resources_for_disabled_categories(self):
        resources = self._get_resources()
        return [r for r in resources if r.get("category") in self.disabled_categories]

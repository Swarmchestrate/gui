import json
import logging
import lxml.html
import os
import random
import requests
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


class Resource:
    type: str
    pk_column_name: str
    _data: dict
    
    def __init__(
            self,
            data: dict,
            type: str,
            pk_column_name: str):
        self._data = data
        self.type = type
        self.pk_column_name = pk_column_name
    
    @property
    def pk(self) -> int:
        return self._data.get(self.pk_column_name)

    def as_dict(self):
        return self._data


class Definition:
    pk_column_name: str
    required: list[str]
    properties: dict
    _data: dict
    
    def __init__(self, data: dict):
        self._data = data
        self.required = data.get("required", [])
        self.properties = data.get("properties", {})
        self.pk_column_name = self._find_pk_column_name()

    def _find_pk_column_name(self):
        for property_name, property_metadata in self.properties.items():
            if "description" not in property_metadata:
                continue
            description = property_metadata.get("description")
            is_pk = lxml.html.fromstring(description).xpath("pk")
            if not is_pk:
                continue
            return property_name
        return None

    def as_dict(self):
        return self._data


class Endpoint:
    table_name: str
    resource_type: None
    definition: Definition

    random_id_min_value: int = 0
    random_id_max_value: int = 999999
    
    def __init__(self, table_name: str, definition: Definition):
        self.table_name = table_name
        self.resource_type = table_name
        self.api_url = os.environ.get("API_URL")
        self.endpoint_url = f"{self.api_url}{table_name}"
        self.definition = definition

    # Error handling
    def log_and_raise_response_status_if_error(self, response: requests.Response):
        if response.ok:
            return
        try:
            logger.error(json.dumps(response.json(), indent=2))
        except Exception:
            logger.exception("Could not log error response.")
        response.raise_for_status()

    # Helper methods
    def _clean_data(self, uncleaned_data: dict) -> dict:
        uncleaned_data_copy = dict(uncleaned_data)
        allowed_properties = self.definition.properties.keys()
        for key in uncleaned_data.keys():
            if key in allowed_properties:
                continue
            uncleaned_data_copy.pop(key)
        return uncleaned_data_copy

    def _get_existing_resource_ids(self):
        params = {"select": f"{self.definition.pk_column_name}"}
        return [
            data.get(self.definition.pk_column_name)
            for data in self.get_resources(params=params)
        ]

    def _generate_random_id(self) -> int:
        existing_resource_ids = self._get_existing_resource_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_resource_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Exception("There are no new unique IDs that can be used.")
        random_id = random.choice(list(possible_ids_set))
        return random_id

    def _generate_random_ids(self, amount: int = 1) -> list[int]:
        existing_resource_ids = self._get_existing_resource_ids()
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        possible_ids_set = set(
            range(self.random_id_min_value, self.random_id_max_value)
        )
        existing_ids_set = set(existing_resource_ids)
        possible_ids_set = possible_ids_set - existing_ids_set
        if not len(possible_ids_set):
            raise Exception("There are no new unique IDs that can be used.")
        random_ids = random.sample(list(possible_ids_set), int(amount))
        if len(random_ids) != amount:
            raise Exception(f"Failed to generate {amount} new unique IDs.")
        return random_ids

    def _set_updated_at_to_now(self, data: dict) -> dict:
        current_time = datetime.now(timezone.utc).isoformat()
        current_time_no_tz = str(current_time).replace("+00:00", "")
        data.update({
            "updated_at": current_time_no_tz,
        })
        return data

    # Main methods
    def get(self, resource_id: int, params: dict | None = None) -> Resource:
        if not params:
            params = dict()
        params.update({
            self.definition.pk_column_name: f"eq.{resource_id}",
        })
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        # Responses are returned as lists, so need
        # to get the first list element.
        resource_unformatted = next(iter(response.json()), None)
        if not resource_unformatted:
            return resource_unformatted
        return Resource(
            resource_unformatted,
            self.resource_type,
            self.definition.pk_column_name
        )

    def get_resources(self, params: dict | None = None) -> list[Resource]:
        if not params:
            params = dict()
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return [
            Resource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in response.json()
        ]

    def get_resources_referencing_resource_id(
            self,
            column_name: str,
            resource_id: int,
            params: dict | None = None) -> list[Resource]:
        if not params:
            params = dict()
        params.update({column_name: f"eq.{int(resource_id)}"})
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return [
            Resource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in response.json()
        ]

    def register(self, data: dict) -> Resource:
        new_id = self._generate_random_id()
        cleaned_data = self._clean_data(data)
        cleaned_data.update({
            self.definition.pk_column_name: new_id,
        })
        response = requests.post(self.endpoint_url, json=cleaned_data)
        self.log_and_raise_response_status_if_error(response)
        new_resource = self.get(new_id)
        return new_resource

    def update(
            self,
            resource_id: int,
            data: dict,
            set_updated_at_to_now: bool = False):
        params = {
            self.definition.pk_column_name: f"eq.{resource_id}",
        }
        if set_updated_at_to_now:
            current_time = datetime.now(timezone.utc).isoformat()
            current_time_no_tz = str(current_time).replace("+00:00", "")
            data.update({
                "updated_at": current_time_no_tz,
            })
        response = requests.patch(self.endpoint_url, params=params, json=data)
        self.log_and_raise_response_status_if_error(response)

    def delete(self, resource_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update({
            self.definition.pk_column_name: f"eq.{resource_id}",
        })
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)

    def delete_many(self, resource_ids: list[int]):
        params = {
            self.definition.pk_column_name: f"in.({','.join(map(str, resource_ids))})",
        }
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)


class OpenApiSpecification:
    def __init__(self, data: dict):
        self._data = data

    def get_definition(self, table_name: str) -> dict:
        return Definition(self._data.get("definitions", {}).get(table_name, {}))

    def get_foreign_key_references_to_table(self, table_name: str) -> dict:
        references = dict()
        definitions = self._data.get("definitions", {})
        # Go through each definition's properties and find a property
        # description containing XML: <fk table=table_name column="...">
        for definition_name, definition in definitions.items():
            properties = definition.get("properties", {})
            for property_metadata in properties.values():
                if "description" not in property_metadata:
                    continue
                description = property_metadata.get("description")
                if table_name not in description:
                    continue
                fk_table_name = next(iter(
                    lxml.html.fromstring(description).xpath("fk/@table")
                ), None)
                fk_column_name = next(iter(
                    lxml.html.fromstring(description).xpath("fk/@column")
                ), None)
                if not fk_table_name or not fk_column_name:
                    continue
                references.update({
                    definition_name: {
                        "table_name": table_name,
                        "column_name": fk_column_name,
                    }
                })
        return references

    def as_dict(self) -> dict:
        return self._data


class ApiClient:
    def __init__(self):
        self.api_url = os.environ.get("API_URL")
        self.openapi_spec = OpenApiSpecification(
            requests.get(self.api_url).json()
        )
    
    def get_endpoint(self, table_name: str) -> Endpoint:
        return Endpoint(
            table_name,
            self.openapi_spec.get_definition(table_name)
        )
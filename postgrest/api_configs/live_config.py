import json
import logging
import os
import requests
from datetime import datetime, timezone

from .base_config import (
    BaseApiClient,
    BaseDefinition,
    BaseEndpoint,
    BaseOpenApiSpecification,
    BaseResource,
)


logger = logging.getLogger(__name__)


class LiveEndpoint(BaseEndpoint):
    def __init__(self, table_name: str, definition: BaseDefinition):
        super().__init__(table_name, definition)
        self.api_url = os.environ.get("API_URL")
        self.endpoint_url = f"{self.api_url}{table_name}"

    # Error handling
    def log_and_raise_response_status_if_error(self, response: requests.Response):
        if response.ok:
            return
        try:
            logger.error(json.dumps(response.json(), indent=2))
        except Exception:
            logger.exception("Could not log error response.")
        response.raise_for_status()

    # Main methods
    def get(self, resource_id: int, params: dict | None = None) -> BaseResource:
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
        return BaseResource(
            resource_unformatted,
            self.resource_type,
            self.definition.pk_column_name
        )

    def get_by_composite_key(self, composite_key: dict) -> BaseResource:
        params = {
            property_name: f"eq.{value}"
            for property_name, value in composite_key.items()
        }
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)

    def get_resources(self, params: dict | None = None) -> list[BaseResource]:
        if not params:
            params = dict()
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return [
            BaseResource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in response.json()
        ]

    def get_resources_by_type(self, type: str, params: dict | None = None) -> list[BaseResource]:
        if not params:
            params = dict()
        params.update({
            "resource_type": f"eq.{type}"
        })
        response = requests.get(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)
        return [
            BaseResource(
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
            params: dict | None = None) -> list[BaseResource]:
        if not params:
            params = dict()
        params.update({column_name: f"eq.{int(resource_id)}"})
        response = requests.get(self.endpoint_url, params=params)
        try:
            self.log_and_raise_response_status_if_error(response)
        except Exception:
            # Return an empty list so the wizard can continue
            # rendering.
            return []
        return [
            BaseResource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in response.json()
        ]

    def register(self, data: dict) -> BaseResource:
        new_id = self._generate_random_id()
        cleaned_data = self._clean_data(data)
        cleaned_data.update({
            self.definition.pk_column_name: new_id,
        })
        response = requests.post(self.endpoint_url, json=cleaned_data)
        self.log_and_raise_response_status_if_error(response)
        new_resource = self.get(new_id)
        return new_resource

    def register_with_composite_key(
            self,
            composite_key: dict,
            data: dict) -> BaseResource:
        cleaned_data = self._clean_data(data)
        response = requests.post(self.endpoint_url, json=cleaned_data)
        self.log_and_raise_response_status_if_error(response)
        new_resource = self.get_by_composite_key(composite_key)
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

    def update_by_composite_key(self, composite_key: dict, data: dict):
        params = {
            property_name: f"eq.{value}"
            for property_name, value in composite_key.items()
        }
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

    def delete_by_composite_key(self, composite_key: dict):
        params = {
            property_name: f"eq.{value}"
            for property_name, value in composite_key.items()
        }
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)

    def delete_many_by_composite_key(self, composite_key_list: list[dict]):
        or_args = []
        for composite_key in composite_key_list:
            and_args = []
            for property_name, value in composite_key.items():
                and_args.append(
                    f"{property_name}.eq.{value}"
                )
            or_args.append(f"and({",".join(and_args)})")
        params = {
            "or": f"({",".join(or_args)})"
        }
        response = requests.delete(self.endpoint_url, params=params)
        self.log_and_raise_response_status_if_error(response)


class LiveApiClient(BaseApiClient):
    def __init__(self):
        super().__init__()
        self.api_url = os.environ.get("API_URL")

    def _get_openapi_spec(self) -> BaseOpenApiSpecification:
        return BaseOpenApiSpecification(
            requests.get(self.api_url).json()
        )

    def get_endpoint(
            self,
            table_name: str) -> LiveEndpoint:
        if not hasattr(self, "openapi_spec"):
            self.initialise_openapi_spec()
        return LiveEndpoint(table_name, self.openapi_spec.get_definition(table_name))
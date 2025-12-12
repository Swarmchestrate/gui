import json
import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings

from postgrest.base.base_api_clients import (
    BaseApiClient,
    BaseApiClientMixin,
)

logger = logging.getLogger(__name__)


class MockApiClientMixin(BaseApiClientMixin):
    def get_openapi_spec(self) -> dict:
        openapi_spec = None
        cwd = os.getcwd()
        base_dir = settings.BASE_DIR
        os.chdir(base_dir)
        try:
            with open(
                os.path.join(
                    base_dir,
                    "postgrest",
                    "mocks",
                    "jsons",
                    "openapi_spec.json",
                ),
                "r",
            ) as f:
                openapi_spec = json.loads(f.read())
        finally:
            os.chdir(cwd)
        return openapi_spec


class MockApiClient(MockApiClientMixin, BaseApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    path_to_mock_data_dir = os.path.join(
        settings.BASE_DIR, "postgrest", "mocks", "jsons", "definitions"
    )
    path_to_temp_data_dir = os.path.join(
        settings.BASE_DIR, "postgrest", "mocks", "jsons", "data", "temp"
    )

    def __init__(self) -> None:
        super().__init__()
        self.endpoint_definition = self.endpoint_definition_class()
        self.path_to_data = os.path.join(
            self.path_to_mock_data_dir, f"{self.endpoint}.json"
        )
        self.path_to_temp_data = os.path.join(
            self.path_to_temp_data_dir, f"{self.endpoint}.json"
        )

    # Helpers
    def _create_temp_data_if_not_exists(self):
        Path(self.path_to_temp_data_dir).mkdir(parents=True, exist_ok=True)
        temp_data_file = Path(self.path_to_temp_data)
        if temp_data_file.is_file():
            return
        shutil.copyfile(self.path_to_data, self.path_to_temp_data)

    def _get_temp_data_and_create_if_not_exists(self):
        self._create_temp_data_if_not_exists()
        temp_data = None
        with open(self.path_to_temp_data, "r") as f:
            temp_data = json.loads(f.read())
        return temp_data

    def _update_temp_data(self, update_data: list):
        with open(self.path_to_temp_data, "w") as f:
            f.write(json.dumps(update_data, indent=4))

    def _get_resources(self, params: dict | None = None) -> list[dict]:
        resources = self._get_temp_data_and_create_if_not_exists()
        return resources

    # Resources
    def get(self, resource_id: int, params: dict | None = None) -> dict:
        resources = self._get_temp_data_and_create_if_not_exists()
        resource = {}
        for r in resources:
            r_id = r.get(self.endpoint_definition.pk_field_name)
            if not r_id:
                continue
            if not int(r_id) == int(resource_id):
                continue
            resource = r
            break
        return resource

    def get_resources_by_ids(
        self, resource_ids: list[int], params: dict | None = None
    ) -> list[dict]:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        resources = [
            r
            for r in all_resources
            if int(r.get(self.endpoint_definition.pk_field_name)) in resource_ids
        ]
        return resources

    def get_resources_referencing_resource_id(
        self, column_name: str, resource_id: int, params: dict | None = None
    ) -> list[dict]:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        resources = [r for r in all_resources if r.get(column_name) == int(resource_id)]
        return resources

    def get_resources(self, params: dict | None = None) -> list[dict]:
        return self._get_resources(params)

    def _register(self, new_id: int, data: dict) -> dict:
        resources = self._get_temp_data_and_create_if_not_exists()
        cleaned_data = self.clean_data(data)
        cleaned_data.update(
            {
                self.endpoint_definition.pk_field_name: new_id,
            }
        )
        if any(
            int(r.get(self.endpoint_definition.pk_field_name)) == int(new_id)
            for r in resources
        ):
            return {}
        resources.append(cleaned_data)
        self._update_temp_data(resources)
        return cleaned_data

    def register(self, data: dict) -> dict:
        new_id = self._generate_random_id()
        return self._register(new_id, data)

    def register_with_id(self, new_id: int, data: dict) -> dict:
        return self._register(new_id, data)

    def bulk_register(self, data_list: list[dict]) -> list[int]:
        resources = self._get_temp_data_and_create_if_not_exists()
        new_ids = self._generate_random_ids(amount=len(data_list))
        try:
            for i, data in enumerate(data_list):
                cleaned_data = self.clean_data(data)
                cleaned_data.update(
                    {self.endpoint_definition.pk_field_name: new_ids[i]}
                )
        except IndexError:
            raise Error("An error occurred whilst assigning IDs for bulk registration.")
        updated_resources = resources + data_list
        self._update_temp_data(updated_resources)
        return new_ids

    def delete(self, resource_id: int, params: dict | None = None):
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if not (
                int(r.get(self.endpoint_definition.pk_field_name)) == int(resource_id)
            )
        ]
        return self._update_temp_data(updated_resources)

    def delete_many(self, resource_ids: list[int]):
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if int(r.get(self.endpoint_definition.pk_field_name)) not in resource_ids
        ]
        return self._update_temp_data(updated_resources)

    def _prepare_update_data(self, data: dict) -> dict:
        current_time = datetime.now(timezone.utc).isoformat()
        current_time_no_tz = str(current_time).replace("+00:00", "")
        data.update(
            {
                "updated_at": current_time_no_tz,
            }
        )
        return data

    def update(self, resource_id: int, data: dict):
        resource_to_update = self.get(resource_id)
        cleaned_data = self.clean_data(data)
        prepared_update_data = self._prepare_update_data(cleaned_data)
        resource_to_update.update(prepared_update_data)
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if not (
                int(r.get(self.endpoint_definition.pk_field_name)) == int(resource_id)
            )
        ]
        updated_resources.append(resource_to_update)
        return self._update_temp_data(updated_resources)

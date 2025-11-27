import json
import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings

from editor.api.base_api_clients import (
    BaseApiClient,
    BaseApiClientMixin,
    BaseColumnMetadataApiClient,
)
from editor.api.mocks.mock_base_definitions import (
    MockColumnMetadataUserSpecifiableOpenApiDefinition,
)

logger = logging.getLogger(__name__)


class MockApiClientMixin(BaseApiClientMixin):
    def get_openapi_spec(self):
        openapi_spec = None
        cwd = os.getcwd()
        base_dir = settings.BASE_DIR
        os.chdir(base_dir)
        try:
            with open(
                os.path.join(
                    base_dir,
                    "editor",
                    "api",
                    "mocks",
                    "jsons",
                    "data",
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

    path_to_data: os.PathLike | str
    path_to_temp_data_dir: os.PathLike | str

    def __init__(self) -> None:
        super().__init__()
        self.endpoint_definition = self.endpoint_definition_class()
        self.path_to_temp_data = os.path.join(
            self.path_to_temp_data_dir, os.path.basename(self.path_to_data)
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

    # Resources
    def get(self, resource_id: int, params: dict | None = None) -> dict:
        resources = self._get_temp_data_and_create_if_not_exists()
        resource = {}
        for r in resources:
            r_id = r.get(self.endpoint_definition.id_field)
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
            if int(r.get(self.endpoint_definition.id_field)) in resource_ids
        ]
        return resources

    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = self._get_temp_data_and_create_if_not_exists()
        return resources

    def register(self, data: dict) -> dict:
        resources = self._get_temp_data_and_create_if_not_exists()
        new_id = self._generate_random_id()
        data.update(
            {
                self.endpoint_definition.id_field: new_id,
            }
        )
        if any(
            int(r.get(self.endpoint_definition.id_field)) == int(new_id)
            for r in resources
        ):
            return {}
        resources.append(data)
        self._update_temp_data(resources)
        return data

    def bulk_register(self, data_list: list[dict]) -> list[int]:
        resources = self._get_temp_data_and_create_if_not_exists()
        new_ids = self._generate_random_ids(amount=len(data_list))
        try:
            for i, data in enumerate(data_list):
                data.update({self.endpoint_definition.id_field: new_ids[i]})
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
            if not (int(r.get(self.endpoint_definition.id_field)) == int(resource_id))
        ]
        return self._update_temp_data(updated_resources)

    def delete_many(self, resource_ids: list[int]):
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if int(r.get(self.endpoint_definition.id_field)) not in resource_ids
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
        prepared_update_data = self._prepare_update_data(data)
        resource_to_update.update(prepared_update_data)
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if not (int(r.get(self.endpoint_definition.id_field)) == int(resource_id))
        ]
        updated_resources.append(resource_to_update)
        return self._update_temp_data(updated_resources)


class MockColumnMetadataApiClient(MockApiClient, BaseColumnMetadataApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    path_to_data = os.path.join(
        settings.BASE_DIR,
        "editor",
        "api",
        "mocks",
        "jsons",
        "data",
        "column_metadata.json",
    )
    path_to_temp_data_dir = os.path.join(settings.BASE_DIR, "editor", "temp")

    endpoint_definition_class = MockColumnMetadataUserSpecifiableOpenApiDefinition

    def get_resources_by_category(self, category: str):
        resources = self.get_resources()
        return [
            r
            for r in resources
            if (
                r.get("category") not in self.disabled_categories
                and r.get("category") == category
            )
        ]

    def get_by_table_name(self, table_name: str):
        resources = self.get_resources()
        return [
            r
            for r in resources
            if (
                r.get("category") not in self.disabled_categories
                and r.get("table_name") == table_name
            )
        ]

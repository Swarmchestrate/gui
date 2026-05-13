import json
import os
import shutil
from datetime import datetime, timezone
from django.conf import settings
from django.template import Template, Context
from pathlib import Path

from .base_config import (
    BaseApiClient,
    BaseEndpoint,
    BaseOpenApiSpecification,
    BaseResource,
)


BASE_DIR = settings.BASE_DIR


class MockEndpoint(BaseEndpoint):
    # Main methods
    path_to_data_dir = os.path.join(
        settings.BASE_DIR,
        "postgrest",
        "mocks",
        "jsons",
        "data"
    )
    path_to_temp_data_dir = os.path.join(
        path_to_data_dir,
        "temp"
    )

    @property
    def path_to_data(self):
        return os.path.join(self.path_to_data_dir, f"{self.table_name}.json")

    @property
    def path_to_temp_data(self):
        return os.path.join(self.path_to_temp_data_dir, f"{self.table_name}.json")

    # Helpers
    def _create_temp_data_if_not_exists(self):
        Path(self.path_to_temp_data_dir).mkdir(parents=True, exist_ok=True)
        temp_data_file = Path(self.path_to_temp_data)
        if temp_data_file.is_file():
            return
        shutil.copyfile(self.path_to_data, self.path_to_temp_data)

    def _get_temp_data_and_create_if_not_exists(self) -> list[dict]:
        self._create_temp_data_if_not_exists()
        temp_data = None
        with open(self.path_to_temp_data, "r") as f:
            temp_data = json.loads(f.read())
        return temp_data

    def _update_temp_data(self, update_data: list):
        with open(self.path_to_temp_data, "w") as f:
            f.write(json.dumps(update_data, indent=4))

    # Main methods
    def get(self, resource_id: int, params: dict | None = None) -> BaseResource:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        resource_unformatted = None
        for r in all_resources:
            r_id = r.get(self.definition.pk_column_name)
            if not r_id:
                continue
            if not int(r_id) == int(resource_id):
                continue
            resource_unformatted = r
            break
        return BaseResource(
            resource_unformatted,
            self.resource_type,
            self.definition.pk_column_name
        )

    def get_resources(self, params: dict | None = None) -> list[BaseResource]:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        return [
            BaseResource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in all_resources
        ]

    def get_resources_by_type(self, type: str, params: dict | None = None) -> list[BaseResource]:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        return [
            BaseResource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in all_resources
            if resource_unformatted.get("resource_type") == type
        ]

    def get_resources_referencing_resource_id(
            self,
            column_name: str,
            resource_id: int,
            params: dict | None = None) -> list[BaseResource]:
        all_resources = self._get_temp_data_and_create_if_not_exists()
        return [
            BaseResource(
                resource_unformatted,
                self.resource_type,
                self.definition.pk_column_name
            )
            for resource_unformatted in all_resources
            if resource_unformatted.get(column_name) == int(resource_id)
        ]

    def register(self, data: dict) -> BaseResource:
        new_id = self._generate_random_id()
        cleaned_data = self._clean_data(data)
        cleaned_data.update({
            self.definition.pk_column_name: new_id,
        })
        resources = self._get_temp_data_and_create_if_not_exists()
        if any(
            int(r.get(self.definition.pk_column_name)) == int(new_id)
            for r in resources
        ):
            return {}
        resources.append(cleaned_data)
        self._update_temp_data(resources)
        return BaseResource(cleaned_data)

    def update(
            self,
            resource_id: int,
            data: dict,
            set_updated_at_to_now: bool = False):
        if set_updated_at_to_now:
            current_time = datetime.now(timezone.utc).isoformat()
            current_time_no_tz = str(current_time).replace("+00:00", "")
            data.update({
                "updated_at": current_time_no_tz,
            })
        cleaned_data = self._clean_data(data)
        resource_to_update_as_dict = self.get(resource_id).as_dict()
        resource_to_update_as_dict.update(cleaned_data)
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if not (
                int(r.get(self.definition.pk_column_name)) == int(resource_id)
            )
        ]
        updated_resources.append(resource_to_update_as_dict)
        return self._update_temp_data(updated_resources)

    def delete(self, resource_id: int, params: dict | None = None):
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if not (
                int(r.get(self.definition.pk_column_name)) == int(resource_id)
            )
        ]
        return self._update_temp_data(updated_resources)

    def delete_many(self, resource_ids: list[int]):
        resources = self._get_temp_data_and_create_if_not_exists()
        updated_resources = [
            r
            for r in resources
            if int(r.get(self.definition.pk_column_name)) not in resource_ids
        ]
        return self._update_temp_data(updated_resources)


class MockApiClient(BaseApiClient):
    def _generate_mock_openapi_spec(self) -> str:
        """Generates a PostgREST OpenAPI specification
        with mock definitions.

        Returns:
            str: A JSON string of the mock OpenAPI specification.
        """
        # The base file path where all the mock JSON files
        # are stored.
        mock_jsons_dir_path = os.path.join(
            BASE_DIR,
            "postgrest",
            "mocks",
            "jsons"
        )
        # Load the mock definitions.
        definitions = dict()
        mock_definitions_dir_path = os.path.join(
            mock_jsons_dir_path,
            "definitions"
        )
        for filename in os.listdir(mock_definitions_dir_path):
            definition_name = filename.replace(".json", "")
            definition_file_path = os.path.join(
                mock_definitions_dir_path,
                filename
            )
            with open(definition_file_path, "r") as definition_file:
                definitions.update({
                    definition_name: definition_file.read(),
                })
        # Generate the OpenAPI specification using the Django
        # template language.
        mock_openapi_spec_template_path = os.path.join(
            mock_jsons_dir_path,
            "openapi_spec.json.djt"
        )
        mock_openapi_spec_template_string = ""
        with open(mock_openapi_spec_template_path, "r") as openapi_spec_file:
            mock_openapi_spec_template_string = openapi_spec_file.read()
        template = Template(mock_openapi_spec_template_string)
        context = Context({
            "definitions": definitions
        })
        mock_openapi_spec = template.render(context)
        # Neatly format the returned JSON.
        return json.dumps(json.loads(mock_openapi_spec), indent=4)

    def _get_openapi_spec(self) -> BaseOpenApiSpecification:
        return BaseOpenApiSpecification(
            json.loads(self._generate_mock_openapi_spec())
        )

    def get_endpoint(
            self,
            table_name: str) -> MockEndpoint:
        if not hasattr(self, "openapi_spec"):
            self.initialise_openapi_spec()
        return MockEndpoint(table_name, self.openapi_spec.get_definition(table_name))
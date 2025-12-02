from application_behaviours.api.definitions import (
    ApplicationBehaviourUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationBehaviourApiClient(BaseApiClient):
    endpoint = "application_behaviour"


class ApplicationBehaviourApiClient(BaseApplicationBehaviourApiClient, ApiClient):
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition


class ApplicationBehaviourColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_behaviour",
            }
        )
        return super().get_resources(params=params)

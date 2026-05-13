import logging

from .api import ApiClient


logger = logging.getLogger(__name__)


class PostgrestApiTestTeardownHelperMixin:
    table_name: str
    resource_ids_added_during_tests: list[int]

    def initialise_test_teardown_helper_components(self):
        self.resource_ids_added_during_tests = list()

    def delete_resources_added_during_test(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        try:
            api_client.get_endpoint(self.table_name).delete_many(
                self.resource_ids_added_during_tests
            )
        except Exception:
            logging.error(
                "PostgREST-API-related test did not finish tear down cleanly. Some resources registered during the test may not have been deleted."
            )

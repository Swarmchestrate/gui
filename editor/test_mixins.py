from postgrest.base.base_api_clients import ApiClient


class ApiClientTestCaseHelperMixin:
    api_client_class: ApiClient
    api_client: ApiClient

    # unittest.TestCase setUp() hook
    def setUp(self):
        super().setUp()
        self.resource_ids = set()
        self.api_client = self.api_client_class()

    def tearDown(self):
        super().tearDown()
        for resource_id in self.resource_ids:
            self.api_client.delete(resource_id)

    # Helper methods
    def generate_random_id_and_add_to_test_ids(self):
        random_id = self.api_client._generate_random_id()
        self.add_resource_id(random_id)
        return random_id

    def add_resource_id(self, resource_id: int):
        self.resource_ids.add(resource_id)

    def register_with_api_client_for_test(self, data: dict = None):
        if not data:
            data = dict()
        new_resource = self.api_client.register(data)
        pk_field_name = self.api_client.endpoint_definition.pk_field_name
        self.add_resource_id(new_resource.get(pk_field_name))
        return new_resource


class ApplicationApiClientTestCaseHelperMixin(ApiClientTestCaseHelperMixin):
    def register_with_api_client_for_test(self, data: dict = None):
        if not data:
            data = dict()
        data.update(
            {
                "name": f"Application {len(self.resource_ids) + 1}",
                "container_image": "https://hub.docker.com/myorg/weather-analytics:latest",
            }
        )
        return super().register_with_api_client_for_test(data)

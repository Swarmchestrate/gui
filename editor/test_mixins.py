from editor.api.endpoints.base import ApiEndpoint


class ApiEndpointTestCaseHelperMixin:
    api_endpoint_client_class: ApiEndpoint
    api_endpoint_client: ApiEndpoint

    # unittest.TestCase setUp() hook
    def setUp(self):
        super().setUp()
        self.registration_ids = set()
        self.api_endpoint_client = self.api_endpoint_client_class()

    def tearDown(self):
        super().tearDown()
        for registration_id in self.registration_ids:
            self.api_endpoint_client.delete(registration_id)

    # Helper methods
    def generate_random_id_and_add_to_test_ids(self):
        random_id = self.api_endpoint_client._generate_random_id()
        self.add_registration_id(random_id)
        return random_id

    def add_registration_id(self, registration_id: int):
        self.registration_ids.add(registration_id)

    def register_with_api_endpoint_client_for_test(self, data: dict = None):
        if not data:
            data = dict()
        new_registration = self.api_endpoint_client.register(data)
        id_field = self.api_endpoint_client.endpoint_definition.id_field
        self.add_registration_id(new_registration.get(id_field))
        return new_registration


class ApplicationApiEndpointTestCaseHelperMixin(ApiEndpointTestCaseHelperMixin):
    def register_with_api_endpoint_client_for_test(self, data: dict = None):
        if not data:
            data = dict()
        data.update(
            {
                "name": f"Application {len(self.registration_ids) + 1}",
                "container_image": "https://hub.docker.com/myorg/weather-analytics:latest",
            }
        )
        return super().register_with_api_endpoint_client_for_test(data)

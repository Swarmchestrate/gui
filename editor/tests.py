from django.test import SimpleTestCase

from editor.api.base_api_clients import ApiClient


class ApiEndpointTestCase(SimpleTestCase):
    def test_get_schema(self):
        client = ApiClient()
        schema = client.get_openapi_spec()
        self.assertIsInstance(schema, dict)

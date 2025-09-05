from django.test import SimpleTestCase

from editor.api_endpoint_client import ApiClient


class ApiEndpointClientTestCase(SimpleTestCase):
    def test_get_schema(self):
        client = ApiClient()
        schema = client.get_openapi_spec()
        self.assertIsInstance(schema, dict)

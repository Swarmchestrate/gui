from django.test import SimpleTestCase

from editor.api_endpoint_client import ColumnMetadataApiEndpointClient


class ApiEndpointClientTestCase(SimpleTestCase):
    def test_get_schema(self):
        client = ColumnMetadataApiEndpointClient()
        schema = client.get_openapi_spec()
        self.assertIsInstance(schema, dict)

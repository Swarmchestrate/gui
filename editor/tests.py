from django.test import SimpleTestCase

from editor.api_endpoint_client import ColumnMetadataApiEndpoint


class ApiEndpointTestCase(SimpleTestCase):
    def test_get_schema(self):
        client = ColumnMetadataApiEndpoint()
        schema = client.get_openapi_spec()
        self.assertIsInstance(schema, dict)

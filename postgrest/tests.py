import json
from django.test import SimpleTestCase

from .new_api import ApiClient, OpenApiSpecification
from .mock_api import generate_mock_openapi_spec

# Create your tests here.
class ApiClientTestCase(SimpleTestCase):
    def test_api_client(self):
        api_client = ApiClient()
        self.assertFalse(hasattr(api_client, "openapi_schema"))
        api_client.initialise_openapi_spec()
        schema = api_client.openapi_spec
        self.assertIsInstance(schema, OpenApiSpecification)


class MockDataTestCase(SimpleTestCase):
    def test_mock_openapi_spec(self):
        mock_openapi_spec = generate_mock_openapi_spec()
        print("mock_openapi_spec", mock_openapi_spec)
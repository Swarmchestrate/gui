import json
from django.test import SimpleTestCase

from .api import ApiClient
from .api_configs.mock_config import MockApiClient
from .api_configs.base_config import BaseApiClient, BaseOpenApiSpecification

# Create your tests here.
class ApiClientTestCase(SimpleTestCase):
    def test_api_client(self):
        api_client = ApiClient()
        self.assertIsInstance(api_client, BaseApiClient)
        self.assertFalse(hasattr(api_client, "openapi_schema"))
        api_client.initialise_openapi_spec()
        schema = api_client.openapi_spec
        self.assertIsInstance(schema, BaseOpenApiSpecification)


class MockDataTestCase(SimpleTestCase):
    def test_mock_openapi_spec(self):
        mock_openapi_spec = MockApiClient()._generate_mock_openapi_spec()
        print("mock_openapi_spec", mock_openapi_spec)
from django.test import SimpleTestCase

from .new_api import ApiClient, OpenApiSpecification

# Create your tests here.
class ApiClientTestCase(SimpleTestCase):
    def test_api_client(self):
        api_client = ApiClient()
        self.assertFalse(hasattr(api_client, "openapi_schema"))
        api_client.initialise_openapi_spec()
        schema = api_client.openapi_spec
        self.assertIsInstance(schema, OpenApiSpecification)
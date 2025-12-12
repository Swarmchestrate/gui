from django.test import SimpleTestCase

from postgrest.base.base_api_clients import ApiClientMixin


class ApiClientTestCase(SimpleTestCase):
    def test_get_schema(self):
        client = ApiClientMixin()
        schema = client.get_openapi_spec()
        self.assertIsInstance(schema, dict)

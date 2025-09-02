import json

from django.test import SimpleTestCase

from .api_client import CapacityApiClient


class CapacityApiClientTestCase(SimpleTestCase):
    def test_get_capacities(self):
        client = CapacityApiClient()
        capacities = client.get_registered_capacities()
        self.assertIsInstance(capacities, list)

    def test_get_fields_with_format(self):
        client = CapacityApiClient()
        example_format = 'text'
        fields = client.get_fields_with_format(example_format)
        self.assertIsInstance(fields, dict)
        self.assertGreater(len(fields.keys()), 0)
        for value in fields.values():
            self.assertEqual(value.get('format'), example_format)

    def test_get_field_formats(self):
        client = CapacityApiClient()
        field_formats = client.get_field_formats()
        self.assertIsInstance(field_formats, list)
import json

from django.test import SimpleTestCase

from .api_client import (
    CapacityApiClient,
    CloudCapacityApiClient,
    EdgeCapacityApiClient,
)


class CapacityApiClientTestCase(SimpleTestCase):
    def test_get(self):
        client = CapacityApiClient()
        capacities = client.get_registrations()
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


class CloudCapacityApiClientTestCase(SimpleTestCase):
    def test_get_registrations(self):
        client = CloudCapacityApiClient()
        capacities = client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        client = CloudCapacityApiClient()
        data = {
            'capacity_id': 5,
        }
        client.register(data)

    def test_delete(self):
        client = CloudCapacityApiClient()
        id = 5
        client.delete(id)


class EdgeCapacityApiClientTestCase(SimpleTestCase):
    def test_get_registrations(self):
        client = EdgeCapacityApiClient()
        capacities = client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        client = EdgeCapacityApiClient()
        data = {
            'capacity_id': 5,
        }
        client.register(data)

    def test_delete(self):
        client = EdgeCapacityApiClient()
        id = 5
        client.delete(id)
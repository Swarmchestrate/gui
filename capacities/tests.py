import json

from django.test import SimpleTestCase

from .api_client import (
    CapacityApiClient,
    CloudCapacityApiClient,
    EdgeCapacityApiClient,
)


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


class CloudCapacityApiClientTestCase(SimpleTestCase):
    def test_get_cloud_capacities(self):
        client = CloudCapacityApiClient()
        capacities = client.get_registered_cloud_capacities()
        self.assertIsInstance(capacities, list)

    def test_register_cloud_capacity(self):
        client = CloudCapacityApiClient()
        data = {
            'capacity_id': 5,
        }
        client.register_cloud_capacity(data)

    def test_delete_cloud_capacity(self):
        client = CloudCapacityApiClient()
        id = 5
        client.delete_cloud_capacity(id)


class EdgeCapacityApiClientTestCase(SimpleTestCase):
    def test_get_edge_capacities(self):
        client = EdgeCapacityApiClient()
        capacities = client.get_registered_edge_capacities()
        self.assertIsInstance(capacities, list)

    def test_register_cloud_capacity(self):
        client = EdgeCapacityApiClient()
        data = {
            'capacity_id': 5,
        }
        client.register_edge_capacity(data)

    def test_delete_edge_capacity(self):
        client = EdgeCapacityApiClient()
        id = 5
        client.delete_edge_capacity(id)
import json

from django.test import SimpleTestCase

from .api_client import (
    CapacityApiClient,
    CloudCapacityApiClient,
    EdgeCapacityApiClient,
)

from editor.test_mixins import ApiClientTestCaseHelperMixin


class CapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = CapacityApiClient

    def test_get_registrations(self):
        capacities = self.api_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_get_fields_with_format(self):
        example_format = 'text'
        fields = self.api_client.get_fields_with_format(example_format)
        self.assertIsInstance(fields, dict)
        self.assertGreater(len(fields.keys()), 0)
        for value in fields.values():
            self.assertEqual(value.get('format'), example_format)

    def test_get_field_formats(self):
        field_formats = self.api_client.get_field_formats()
        self.assertIsInstance(field_formats, list)


class CloudCapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = CloudCapacityApiClient

    def test_get_registrations(self):
        capacities = self.api_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        data = {
            'capacity_id': self.generate_random_id(),
        }
        self.api_client.register(data)

    def test_delete(self):
        id = self.generate_random_id()
        self.api_client.delete(id)


class EdgeCapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = EdgeCapacityApiClient

    def test_get_registrations(self):
        capacities = self.api_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        data = {
            'capacity_id': self.generate_random_id(),
        }
        self.api_client.register(data)

    def test_delete(self):
        id = self.generate_random_id()
        self.api_client.delete(id)
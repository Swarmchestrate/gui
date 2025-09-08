import json

from django.test import SimpleTestCase

from .api_endpoint_client import (
    CapacityApiEndpointClient,
    CloudCapacityApiEndpointClient,
    EdgeCapacityApiEndpointClient,
)

from editor.test_mixins import ApiEndpointClientTestCaseHelperMixin


class CapacityApiEndpointClientTestCase(ApiEndpointClientTestCaseHelperMixin, SimpleTestCase):
    api_endpoint_client_class = CapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_get_user_specifiable_fields_with_format(self):
        example_format = 'text'
        fields = self.api_endpoint_client.endpoint_definition.get_user_specifiable_fields_with_format(example_format)
        self.assertIsInstance(fields, dict)
        self.assertGreater(len(fields.keys()), 0)
        for value in fields.values():
            self.assertEqual(value.get('format'), example_format)

    def test_get_user_specifiable_field_formats(self):
        field_formats = self.api_endpoint_client.endpoint_definition.get_user_specifiable_field_formats()
        self.assertIsInstance(field_formats, list)


class CloudCapacityApiEndpointClientTestCase(ApiEndpointClientTestCaseHelperMixin, SimpleTestCase):
    api_endpoint_client_class = CloudCapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        data = {
            'capacity_id': self.generate_random_id_and_add_to_test_ids(),
        }
        self.api_endpoint_client.register(data)

    def test_delete(self):
        id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint_client.delete(id)


class EdgeCapacityApiEndpointClientTestCase(ApiEndpointClientTestCaseHelperMixin, SimpleTestCase):
    api_endpoint_client_class = EdgeCapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        data = {
            'capacity_id': self.generate_random_id_and_add_to_test_ids(),
        }
        new_registration = self.api_endpoint_client.register(data)
        self.assertIsInstance(new_registration, dict)

    def test_delete(self):
        id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint_client.delete(id)
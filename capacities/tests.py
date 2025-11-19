from django.test import SimpleTestCase

from editor.mixins.test_mixins import ApiEndpointClientTestCaseHelperMixin

from .api_endpoint_client import (
    CapacityApiEndpointClient,
    CloudCapacityApiEndpointClient,
    EdgeCapacityApiEndpointClient,
)


class CapacityApiEndpointClientTestCase(
    ApiEndpointClientTestCaseHelperMixin, SimpleTestCase
):
    api_endpoint_client_class = CapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_get_user_specifiable_fields_with_format(self):
        example_format = "text"
        fields = self.api_endpoint_client.endpoint_definition.get_user_specifiable_fields_with_format(
            example_format
        )
        self.assertIsInstance(fields, dict)
        self.assertGreater(len(fields.keys()), 0)
        for value in fields.values():
            self.assertEqual(value.get("format"), example_format)

    def test_get_user_specifiable_field_formats(self):
        field_formats = self.api_endpoint_client.endpoint_definition.get_user_specifiable_field_formats()
        self.assertIsInstance(field_formats, list)


class CloudCapacityApiEndpointClientTestCase(
    ApiEndpointClientTestCaseHelperMixin, SimpleTestCase
):
    api_endpoint_client_class = CloudCapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        new_registration = self.api_endpoint_client.register()
        self.assertIsInstance(new_registration, dict)

    def test_delete(self):
        registration_id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint_client.delete(registration_id)

    def test_update(self):
        # Test setup
        new_registration = self.register_with_api_endpoint_client_for_test()
        self.assertEqual(new_registration.get("mobility"), None)
        # Update
        update_data = {
            "mobility": True,
        }
        id_field = self.api_endpoint_client.endpoint_definition.id_field
        self.api_endpoint_client.update(new_registration.get(id_field), update_data)
        updated_registration = self.api_endpoint_client.get(
            new_registration.get(id_field)
        )
        self.assertEqual(updated_registration.get("mobility"), True)


class EdgeCapacityApiEndpointClientTestCase(
    ApiEndpointClientTestCaseHelperMixin, SimpleTestCase
):
    api_endpoint_client_class = EdgeCapacityApiEndpointClient

    def test_get_registrations(self):
        capacities = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        new_registration = self.api_endpoint_client.register()
        self.assertIsInstance(new_registration, dict)

    def test_delete(self):
        registration_id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint_client.delete(registration_id)

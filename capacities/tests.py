from django.test import SimpleTestCase

from editor.test_mixins import ApiClientTestCaseHelperMixin

from .api.capacity_api_clients import CapacityApiClient
from .api.cloud_capacity_api_clients import CloudCapacityApiClient
from .api.edge_capacity_api_clients import EdgeCapacityApiClient


class CapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = CapacityApiClient

    def test_get_resources(self):
        capacities = self.api_client.get_resources()
        self.assertIsInstance(capacities, list)

    def test_get_user_specifiable_fields_with_format(self):
        example_format = "text"
        fields = (
            self.api_client.endpoint_definition.get_user_specifiable_fields_with_format(
                example_format
            )
        )
        self.assertIsInstance(fields, dict)
        self.assertGreater(len(fields.keys()), 0)
        for value in fields.values():
            self.assertEqual(value.get("format"), example_format)

    def test_get_user_specifiable_field_formats(self):
        field_formats = (
            self.api_client.endpoint_definition.get_user_specifiable_field_formats()
        )
        self.assertIsInstance(field_formats, list)


class CloudCapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = CloudCapacityApiClient

    def test_get_resources(self):
        capacities = self.api_client.get_resources()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        new_resource = self.api_client.register()
        self.assertIsInstance(new_resource, dict)

    def test_delete(self):
        resource_id = self.generate_random_id_and_add_to_test_ids()
        self.api_client.delete(resource_id)

    def test_update(self):
        # Test setup
        new_resource = self.register_with_api_client_for_test()
        self.assertEqual(new_resource.get("mobility"), None)
        # Update
        update_data = {
            "mobility": True,
        }
        id_field = self.api_client.endpoint_definition.id_field
        self.api_client.update(new_resource.get(id_field), update_data)
        updated_resource = self.api_client.get(new_resource.get(id_field))
        self.assertEqual(updated_resource.get("mobility"), True)


class EdgeCapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = EdgeCapacityApiClient

    def test_get_resources(self):
        capacities = self.api_client.get_resources()
        self.assertIsInstance(capacities, list)

    def test_register(self):
        new_resource = self.api_client.register()
        self.assertIsInstance(new_resource, dict)

    def test_delete(self):
        resource_id = self.generate_random_id_and_add_to_test_ids()
        self.api_client.delete(resource_id)

from django.test import SimpleTestCase

from editor.test_mixins import ApiClientTestCaseHelperMixin
from postgrest.mocks.mock_api_clients import (
    CloudCapacityApiClient,
    EdgeCapacityApiClient,
)


class CapacityApiClientTestCase(ApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = CloudCapacityApiClient

    def test_get_resources(self):
        capacities = self.api_client.get_resources()
        self.assertIsInstance(capacities, list)


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
        pk_field_name = self.api_client.endpoint_definition.pk_field_name
        self.api_client.update(new_resource.get(pk_field_name), update_data)
        updated_resource = self.api_client.get(new_resource.get(pk_field_name))
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

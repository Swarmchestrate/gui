from django.test import SimpleTestCase

from .tosca import generate_capacity_description_template

from postgrest.api import ApiClient, Resource
from postgrest.test_mixins import PostgrestApiTestTeardownHelperMixin


class CapacityPostgrestApiTestCase(
        PostgrestApiTestTeardownHelperMixin,
        SimpleTestCase):
    table_name = "capacity_new"
    
    def setUp(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        self.endpoint = api_client.get_endpoint(self.table_name)
        self.initialise_test_teardown_helper_components()
        return super().setUp()

    def tearDown(self):
        self.delete_resources_added_during_test()
        return super().tearDown()

    def test_get_resources(self):
        capacities = self.endpoint.get_resources()
        self.assertIsInstance(capacities, list)
        if len(capacities) > 0:
            self.assertTrue(all(
                isinstance(resource, Resource)
                for resource in capacities
            ))

    def test_register(self):
        new_resource = self.endpoint.register({})
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.assertIsInstance(new_resource, Resource)

    def test_delete(self):
        new_resource = self.endpoint.register({})
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.endpoint.delete(new_resource.pk)

    def test_update(self):
        TEST_PROPERTY = "description"
        TEST_CONTENT = "Updated"
        # Register new resource for testing
        new_resource = self.endpoint.register({})
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.assertEqual(new_resource.as_dict().get(TEST_PROPERTY), None)
        # Test update is applied
        update_data = {
            TEST_PROPERTY: TEST_CONTENT,
        }
        self.endpoint.update(new_resource.pk, update_data)
        updated_resource = self.endpoint.get(new_resource.pk)
        self.assertEqual(
            updated_resource.as_dict().get(TEST_PROPERTY),
            TEST_CONTENT
        )


class CapacityDescriptionTemplateTestCase(
        PostgrestApiTestTeardownHelperMixin,
        SimpleTestCase):
    table_name = "capacity_new"
    
    def setUp(self):
        self.initialise_test_teardown_helper_components()
        return super().setUp()

    def tearDown(self):
        self.delete_resources_added_during_test()
        return super().tearDown()

    def test_capacity_description_template_generation(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        endpoint = api_client.get_endpoint(self.table_name)
        new_resource = endpoint.register({})
        self.resource_ids_added_during_tests.append(new_resource.pk)
        cdt = generate_capacity_description_template(new_resource.pk)
        self.assertIsInstance(cdt, str)


from django.test import SimpleTestCase

from postgrest.new_api import ApiClient, Resource
from postgrest.test_mixins import PostgrestApiTestTeardownHelperMixin


class ApplicationApiClientTestCase(
        PostgrestApiTestTeardownHelperMixin,
        SimpleTestCase):
    table_name = "application_new"
    TEST_REGISTRATION_DATA = {
        "name": "Weather Analytics App",
        "container_image": "https://hub.docker.com/myorg/weather-analytics:latest",
    }
    
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
        applications = self.endpoint.get_resources()
        self.assertIsInstance(applications, list)
        if len(applications) > 0:
            self.assertTrue(all(
                isinstance(resource, Resource)
                for resource in applications
            ))

    def test_register(self):
        new_resource = self.endpoint.register(self.TEST_REGISTRATION_DATA)
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.assertIsInstance(new_resource, Resource)

    def test_delete(self):
        new_resource = self.endpoint.register(self.TEST_REGISTRATION_DATA)
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.endpoint.delete(new_resource.pk)

    def test_update(self):
        TEST_PROPERTY = "name"
        TEST_CONTENT = "Updated"
        # Register new resource for testing
        new_resource = self.endpoint.register(self.TEST_REGISTRATION_DATA)
        self.resource_ids_added_during_tests.append(new_resource.pk)
        self.assertEqual(
            new_resource.as_dict().get(TEST_PROPERTY),
            self.TEST_REGISTRATION_DATA.get(TEST_PROPERTY)
        )
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

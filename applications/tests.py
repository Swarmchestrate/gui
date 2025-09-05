import json

from django.test import SimpleTestCase

from .api_endpoint_client import ApplicationApiEndpointClient

from editor.test_mixins import ApplicationApiEndpointClientTestCaseHelperMixin


class ApplicationApiEndpointClientTestCase(ApplicationApiEndpointClientTestCaseHelperMixin, SimpleTestCase):
    api_endpoint_client_class = ApplicationApiEndpointClient

    def test_get_registrations(self):
        applications = self.api_endpoint_client.get_registrations()
        self.assertIsInstance(applications, list)

    def test_register(self):
        data = {
            'application_id': self.generate_random_id_and_add_to_test_ids(),
            'name': 'Weather Analytics App',
            'container_image': 'https://hub.docker.com/myorg/weather-analytics:latest',
        }
        self.api_endpoint_client.register(data)

    def test_delete(self):
        id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint_client.delete(id)
import json

from django.test import SimpleTestCase

from .api_client import ApplicationApiClient

from editor.test_mixins import ApplicationApiClientTestCaseHelperMixin


class ApplicationApiClientTestCase(ApplicationApiClientTestCaseHelperMixin, SimpleTestCase):
    api_client_class = ApplicationApiClient

    def test_get_registrations(self):
        applications = self.api_client.get_registrations()
        self.assertIsInstance(applications, list)

    def test_register(self):
        data = {
            'application_id': self.generate_random_id_and_add_to_test_ids(),
            'name': 'Weather Analytics App',
            'container_image': 'https://hub.docker.com/myorg/weather-analytics:latest',
        }
        self.api_client.register(data)

    def test_delete(self):
        id = self.generate_random_id_and_add_to_test_ids()
        self.api_client.delete(id)
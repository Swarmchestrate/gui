import json

from django.test import SimpleTestCase

from .api_client import ApplicationApiClient


class ApplicationApiClientTestCase(SimpleTestCase):
    def test_get_registrations(self):
        client = ApplicationApiClient()
        applications = client.get_registrations()
        self.assertIsInstance(applications, list)

    def test_register(self):
        client = ApplicationApiClient()
        data = {
            'application_id': 5,
            'name': 'Weather Analytics App',
            'container_image': 'https://hub.docker.com/myorg/weather-analytics:latest',
        }
        client.register(data)

    def test_delete(self):
        client = ApplicationApiClient()
        id = 5
        client.delete(id)
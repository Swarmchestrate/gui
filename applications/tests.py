import json

from django.test import SimpleTestCase

from editor.test_mixins import ApplicationApiClientTestCaseHelperMixin

from .api.api_clients import ApplicationApiClient


class ApplicationApiClientTestCase(
    ApplicationApiClientTestCaseHelperMixin, SimpleTestCase
):
    api_client_class = ApplicationApiClient

    def test_get_resources(self):
        applications = self.api_client.get_resources()
        self.assertIsInstance(applications, list)

    def test_register(self):
        data = {
            "name": "Weather Analytics App",
            "container_image": "https://hub.docker.com/myorg/weather-analytics:latest",
        }
        self.api_client.register(data)

    def test_delete(self):
        resource_id = self.generate_random_id_and_add_to_test_ids()
        self.api_client.delete(resource_id)

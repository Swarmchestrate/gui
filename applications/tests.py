import json

from django.test import SimpleTestCase

from editor.test_mixins import ApplicationApiEndpointTestCaseHelperMixin

from .api.endpoints.application import ApplicationApiEndpoint


class ApplicationApiEndpointTestCase(
    ApplicationApiEndpointTestCaseHelperMixin, SimpleTestCase
):
    api_endpoint_class = ApplicationApiEndpoint

    def test_get_registrations(self):
        applications = self.api_endpoint.get_registrations()
        self.assertIsInstance(applications, list)

    def test_register(self):
        data = {
            "name": "Weather Analytics App",
            "container_image": "https://hub.docker.com/myorg/weather-analytics:latest",
        }
        self.api_endpoint.register(data)

    def test_delete(self):
        registration_id = self.generate_random_id_and_add_to_test_ids()
        self.api_endpoint.delete(registration_id)

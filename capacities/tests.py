from django.test import SimpleTestCase

from .api_client import CapacityApiClient


class CapacityApiClientTestCase(SimpleTestCase):
    def test_get_capacities(self):
        client = CapacityApiClient()
        capacities = client.get_registered_capacities()
        self.assertIsInstance(capacities, list)
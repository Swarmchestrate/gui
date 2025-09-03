import random

from .api_client import ApiClient


class ApiClientTestCaseHelperMixin:
    api_client_class: ApiClient
    api_client: ApiClient

    # unittest.TestCase setUp() hook
    def setUp(self):
        super().setUp()
        # Corresponds to Postgres Integer range
        self.random_id_min_value = 0
        self.random_id_max_value = 999
        self.registration_ids = set()
        self.api_client = self.api_client_class()

    def tearDown(self):
        super().tearDown()
        for registration_id in self.registration_ids:
            self.api_client.delete(registration_id)

    # Helper methods
    def _get_existing_registration_ids(self):
        params = {
            'select': f'{self.api_client.id_field}'
        }
        return [
            data.get(self.api_client.id_field)
            for data in self.api_client.get_registrations(params=params)
        ]

    def generate_random_id(self):
        existing_registration_ids = self._get_existing_registration_ids() + list(self.registration_ids)
        # Credit for random_id solution: https://stackoverflow.com/a/70239671
        random_id = random.choice(list(
            set([x for x in range(self.random_id_min_value, self.random_id_max_value)]) - set(existing_registration_ids)
        ))
        self.add_registration_id(random_id)
        return random_id

    def add_registration_id(self, registration_id: int):
        self.registration_ids.add(registration_id)

    def register_with_api_client_for_test(self, data: dict = dict()):
        random_id = self.generate_random_id()
        data.update({
            self.api_client.id_field: random_id,
        })
        self.api_client.register(data)
        registration = self.api_client.get(random_id)
        return registration


class ApplicationApiClientTestCaseHelperMixin(ApiClientTestCaseHelperMixin):
    def register_with_api_client_for_test(self, data: dict = dict()):
        data.update({
            'name': f'Application {len(self.registration_ids) + 1}',
            'container_image': 'https://hub.docker.com/myorg/weather-analytics:latest',
        })
        return super().register_with_api_client_for_test(data)
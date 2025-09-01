import requests

from editor.api_client import ApiClient


class CapacityApiClient(ApiClient):
    def get_registered_capacities(self):
        response = requests.get(f'{self.api_url}/capacity')
        response.raise_for_status()
        return response.json()

    def register_capacity(self, data: dict):
        response = requests.post(f'{self.api_url}/capacity', data=data)
        response.raise_for_status()
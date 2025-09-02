import requests

from editor.api_client import ApiClient


class BaseCapacityApiClient(ApiClient):
    def __init__(self) -> None:
        super().__init__()
        self.definition_name = 'capacity'
        self.endpoint = 'capacity'


class CapacityApiClient(BaseCapacityApiClient):
    def get_registered_capacities(self):
        response = requests.get(f'{self.api_url}/{self.endpoint}')
        response.raise_for_status()
        return response.json()

    def register_capacity(self, data: dict):
        response = requests.post(f'{self.api_url}/{self.endpoint}', data=data)
        response.raise_for_status()


class CloudCapacityApiClient(BaseCapacityApiClient):
    def get_registered_cloud_capacities(self):
        response = requests.get(f'{self.endpoint_url}?resource_type=eq.Cloud')
        response.raise_for_status()
        return response.json()

    def register_cloud_capacity(self, data: dict):
        data.update({
            'resource_type': 'Cloud',
        })
        response = requests.post(self.endpoint_url, data=data)
        response.raise_for_status()

    def delete_cloud_capacity(self, id: int):
        response = requests.delete(f'{self.endpoint_url}?capacity_id=eq.{id}&resource_type=eq.Cloud')
        response.raise_for_status()


class EdgeCapacityApiClient(BaseCapacityApiClient):
    def get_registered_edge_capacities(self):
        response = requests.get(f'{self.endpoint_url}?resource_type=eq.Edge')
        response.raise_for_status()
        return response.json()

    def register_edge_capacity(self, data: dict):
        data.update({
            'resource_type': 'Edge',
        })
        response = requests.post(f'{self.api_url}/{self.endpoint}', data=data)
        response.raise_for_status()

    def delete_edge_capacity(self, id: int):
        response = requests.delete(f'{self.endpoint_url}?capacity_id=eq.{id}&resource_type=eq.Edge')
        response.raise_for_status()
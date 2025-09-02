import requests

from editor.api_client import ApiClient


class ApplicationApiClient(ApiClient):
    def __init__(self) -> None:
        super().__init__()
        self.definition_name = 'application'
        self.endpoint = 'application'

    def get_registered_applications(self):
        response = requests.get(f'{self.api_url}/{self.endpoint}')
        response.raise_for_status()
        return response.json()

    def register_application(self, data: dict):
        response = requests.post(f'{self.api_url}/{self.endpoint}', data=data)
        response.raise_for_status()
import os
import requests


class ApiClient:
    def __init__(self) -> None:
        self.api_url = os.environ.get('API_URL')
        self.openapi_spec_url = os.environ.get('OPENAPI_SPEC_URL')

    def get_openapi_spec(self):
        return requests.get(self.api_url)
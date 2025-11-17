import json
import os
import requests

from django.conf import settings

from ..api_client import ApiClient


class TestApiClient(ApiClient):
    def log_and_raise_response_status_if_error(self, response: requests.Response):
        pass

    def get_openapi_spec(self):
        openapi_spec = None
        cwd = os.getcwd()
        base_dir = settings.BASE_DIR
        os.chdir(base_dir)
        try:
            with open(os.path.join(
                base_dir,
                'editor',
                'mocks',
                'openapi_spec.json'
            ), 'r') as f:
                openapi_spec = json.loads(f.read())
        finally:
            os.chdir(cwd)
        return openapi_spec

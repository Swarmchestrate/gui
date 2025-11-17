import json
import logging
import os
import requests
from prance import ResolvingParser


logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self) -> None:
        self.api_url = os.environ.get('API_URL')

    def log_and_raise_response_status_if_error(self, response: requests.Response):
        if response.ok:
            return
        try:
            logger.error(json.dumps(response.json(), indent=2))
        except Exception:
            logger.exception('Could not log error response.')
        response.raise_for_status()

    def get_openapi_spec(self):
        response = requests.get(self.api_url)
        self.log_and_raise_response_status_if_error(response)
        return response.json()

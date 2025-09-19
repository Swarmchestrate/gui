import json
import logging
import os
import requests
from prance import ResolvingParser

from django.conf import settings


logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self) -> None:
        self.api_url = os.environ.get('API_URL')

    def log_and_raise_response_status_if_error(self, response: requests.Response):
        if response.status_code == requests.codes.ok:
            return
        try:
            logger.error(json.dumps(response.json(), indent=2))
        except TypeError:
            logger.error('Could not parse and log response as JSON.')
        response.raise_for_status()

    def get_openapi_spec(self):
        # TEMP - API spec currently not parsing correctly
        parser = ResolvingParser(os.path.join(settings.BASE_DIR, 'swagger.yaml'))
        return parser.specification
        # response = requests.get(self.api_url)
        # self.log_and_raise_response_status_if_error(response)
        # return response.json()

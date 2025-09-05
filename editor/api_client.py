import os
from prance import ResolvingParser

from django.conf import settings


class ApiClient:
    def __init__(self) -> None:
        self.api_url = os.environ.get('API_URL')

    def get_openapi_spec(self):
        # TEMP - API spec currently not parsing correctly
        parser = ResolvingParser(os.path.join(settings.BASE_DIR, 'swagger.yaml'))
        return parser.specification
        # response = requests.get(self.api_url)
        # response.raise_for_status()
        # return response.json()
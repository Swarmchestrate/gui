import os

from django.conf import settings

from ..api_endpoint_client import BaseCapacityApiEndpointClient
from editor.mocks.api_endpoint_client import (
    TestApiEndpointClient,
    TestColumnMetadataApiEndpointClient,
)

BASE_DIR = settings.BASE_DIR


class CloudCapacityApiEndpointClient(TestApiEndpointClient, BaseCapacityApiEndpointClient):
    path_to_data = os.path.join(
        BASE_DIR,
        'capacities',
        'mocks',
        'data',
        'cloud_capacities.json'
    )
    path_to_temp_data_dir = os.path.join(
        BASE_DIR,
        'capacities',
        'temp'
    )


class CloudCapacityColumnMetadataApiEndpointClient(TestColumnMetadataApiEndpointClient):
    def get_registrations(self, params: dict = None):
        registrations = super().get_registrations()
        return [
            r for r in registrations
            if (
                r.get('table_name') == 'capacity'
                and r.get('category') != 'Edge Specific'
            )
        ]

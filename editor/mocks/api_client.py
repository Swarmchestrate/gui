import json
import os

from django.conf import settings

from editor.api.abc import BaseApiClient


class MockApiClient(BaseApiClient):
    def get_openapi_spec(self):
        openapi_spec = None
        cwd = os.getcwd()
        base_dir = settings.BASE_DIR
        os.chdir(base_dir)
        try:
            with open(
                os.path.join(
                    base_dir, "editor", "mocks", "jsons", "data", "openapi_spec.json"
                ),
                "r",
            ) as f:
                openapi_spec = json.loads(f.read())
        finally:
            os.chdir(cwd)
        return openapi_spec

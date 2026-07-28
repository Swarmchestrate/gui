import os
import requests

from postgrest.api_configs.base_config import build_api_url


def generate_sat(
        data: str,
        params: dict,
        endpoint_path: str) -> dict | None:
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        build_api_url(
            os.environ.get("SAT_BUILDER_API_URL"),
            endpoint_path,
            env_var_name="SAT_BUILDER_API_URL"
        ),
        headers=headers,
        params=params,
        data=data
    )
    sat = None
    sat = response.json()
    return sat
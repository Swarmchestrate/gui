import os
import requests


def generate_sat(
        data: str,
        params: dict,
        endpoint_path: str) -> dict | None:
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        "%s%s" % (
            os.environ.get("SAT_BUILDER_API_URL"),
            endpoint_path
        ),
        headers=headers,
        params=params,
        data=data
    )
    sat = None
    sat = response.json()
    return sat
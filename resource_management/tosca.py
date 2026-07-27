import logging
import os
import requests


logger = logging.getLogger(__name__)


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
    try:
        response.raise_for_status()
    except Exception as err:
        raise err
    return response.json()
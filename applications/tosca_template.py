import json
import os
import yaml

from django.conf import settings
from django.template import Template, Context

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


BASE_DIR = settings.BASE_DIR


def get_data_for_sat(application_id: int) -> dict:
    application_id = int(application_id)
    # Set up API client
    api_client = ApiClient()
    api_client.initialise_openapi_spec()

    # Application
    endpoint = api_client.get_endpoint(TableNames.APPLICATION_NEW)
    application = endpoint.get(application_id)
    application_dict = application.as_dict(include_pk=True)

    # Application - Microservices
    application_microservice_endpoint = api_client.get_endpoint(TableNames.APPLICATION_MICROSERVICE)
    application_microservices = application_microservice_endpoint.get_resources_by_params({
        "application_id": application_id,
    })
    application_microservice_dicts = [
        application_microservice.as_dict(include_pk=True)
        for application_microservice in application_microservices
    ]

    # Application - Volumes
    application_volume_endpoint = api_client.get_endpoint(TableNames.APPLICATION_VOLUME)
    application_volumes = application_volume_endpoint.get_resources_referencing_any_resource_id(
        "application_microservice_id",
        [
            application_microservice.pk
            for application_microservice in application_microservices
        ]
    )
    application_volume_dicts_by_application_microservice = {}
    for i, application_volume in enumerate(application_volumes):
        application_microservice_id = application_volume.as_dict().get("application_microservice_id")
        application_volume_dict = application_volume.as_dict(include_pk=True)
        application_volume_dict.update({
            "__name__": f"volume-{i + 1}",
        })
        application_volume_dicts_by_application_microservice.update({
            application_microservice_id: application_volume_dict,
        })

    # Application - Behaviour
    application_behaviour_endpoint = api_client.get_endpoint(TableNames.APPLICATION_BEHAVIOUR)
    application_behaviour_id = application.as_dict().get("behaviour_id")
    application_behaviour_dict = None
    if application_behaviour_id:
        application_behaviour = application_behaviour_endpoint.get(application_behaviour_id)
        application_behaviour_dict = application_behaviour.as_dict(include_pk=True)

    # Locality
    locality_endpoint = api_client.get_endpoint(TableNames.LOCALITY)
    locality_id = application.as_dict().get("locality_id")
    locality_dict = None
    if locality_id:
        locality = locality_endpoint.get(locality_id)
        locality_dict = locality.as_dict(include_pk=True)
    return {
        "application": application_dict,
        "application_behaviour": application_behaviour_dict,
        "application_microservices": application_microservice_dicts,
        "application_volumes": application_volume_dicts_by_application_microservice,
        "locality": locality_dict,
    }


def generate_adt_yaml(application_id: int) -> str | None:
    data = get_data_for_sat(application_id)
    sat_template_path = os.path.join(
        BASE_DIR,
        "applications",
        "sat_template.yaml.djt"
    )
    sat_template_string = ""
    with open(sat_template_path, "r") as sat_template_file:
        sat_template_string = sat_template_file.read()
    template = Template(sat_template_string)
    context = Context(data)
    data_yaml = template.render(context)
    yaml_as_dict = yaml.safe_load(data_yaml)
    data_json = json.dumps(yaml_as_dict, indent=4, default=str)
    application_description = "This Swarmchestrate Application Template was generated using the Swarmchestrate GUI."
    if data.get("application").get("description"):
        application_description = data.get("application").get("description")
    params = {
        # "response_type": "yaml_and_json",
        "template_version": "latest",
        # "definitions_version": "tosca_3_1",
        "description": application_description,
    }
    sat = generate_sat(
        data_json,
        params,
        "application/build"
    )
    return yaml.dump(sat, default_flow_style=False)
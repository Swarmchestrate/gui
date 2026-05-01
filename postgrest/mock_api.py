import json
import os
from django.conf import settings
from django.template import Template, Context


BASE_DIR = settings.BASE_DIR


def generate_mock_openapi_spec() -> str:
    """Generates a PostgREST OpenAPI specification
    with mock definitions.

    Returns:
        str: A JSON string of the mock OpenAPI specification.
    """
    # The base file path where all the mock JSON files
    # are stored.
    mock_jsons_dir_path = os.path.join(
        BASE_DIR,
        "postgrest",
        "mocks",
        "jsons"
    )
    # Load the mock definitions.
    definitions = dict()
    mock_definitions_dir_path = os.path.join(
        mock_jsons_dir_path,
        "definitions"
    )
    for filename in os.listdir(mock_definitions_dir_path):
        definition_name = filename.replace(".json", "")
        definition_file_path = os.path.join(
            mock_definitions_dir_path,
            filename
        )
        with open(definition_file_path, "r") as definition_file:
            definitions.update({
                definition_name: definition_file.read(),
            })
    # Generate the OpenAPI specification using the Django
    # template language.
    mock_openapi_spec_template_path = os.path.join(
        mock_jsons_dir_path,
        "openapi_spec.json.djt"
    )
    mock_openapi_spec_template_string = ""
    with open(mock_openapi_spec_template_path, "r") as openapi_spec_file:
        mock_openapi_spec_template_string = openapi_spec_file.read()
    template = Template(mock_openapi_spec_template_string)
    context = Context({
        "definitions": definitions
    })
    mock_openapi_spec = template.render(context)
    # Neatly format the returned JSON.
    return json.dumps(json.loads(mock_openapi_spec), indent=4)
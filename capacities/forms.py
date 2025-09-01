from editor.forms import OpenApiSpecBasedForm


class NewCloudCapacityForm(OpenApiSpecBasedForm):
    definition_name = 'capacity'


class NewEdgeCapacityForm(OpenApiSpecBasedForm):
    definition_name = 'capacity'
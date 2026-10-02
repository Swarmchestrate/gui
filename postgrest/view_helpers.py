from .forms.form_config import (
    ColumnMetadata,
    FormConfig,
    Properties,
    OneToManyProperties,
)
from .api import ApiClient, OpenApiSpecification, Resource
from .forms.field_choices import choices_for
from .forms.field_widgets import widget_for
from .table_names import TableNames

from utils.helpers import get_column_metadata_table_name_for_table


class FormConfigViewMixin:
    table_name: str
    api_client: ApiClient
    openapi_spec: OpenApiSpecification
    form_config: FormConfig
    column_metadata: list[Resource]

    def setup(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint(
            TableNames.COLUMN_METADATA
        ).get_resources()
        return super().setup(request, *args, **kwargs)

    def get_form_config(self) -> FormConfig:
        return get_form_config_for_table(
            self.table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            **self.get_form_config_kwargs()
        )

    def get_form_config_kwargs(self) -> dict:
        return dict()


class ForeignKeyTableFormConfigViewMixin(FormConfigViewMixin):
    fk_table_name: str

    def get_fk_table_form_config(self, extra_form_config_kwargs: dict = None) -> FormConfig:
        kwargs = self.get_fk_table_form_config_kwargs()
        if not extra_form_config_kwargs:
            extra_form_config_kwargs = dict()
        if extra_form_config_kwargs:
            kwargs.update(extra_form_config_kwargs)
        return get_form_config_for_table(
            self.fk_table_name,
            self.api_client.openapi_spec,
            self.column_metadata,
            **kwargs
        )

    def get_fk_table_form_config_kwargs(self) -> dict:
        return dict()


def get_form_config_for_table(
        table_name: str,
        openapi_spec: OpenApiSpecification,
        column_metadata_as_list: list[Resource],
        infer_one_to_many_properties: bool = True,
        disabled_properties: list[str] = None,
        choices_context: dict = None) -> FormConfig:
    # A list of additional disabled property names that is passed to the
    # FormConfig and is best specified when inside a view.
    if not disabled_properties:
        disabled_properties = list()
    column_metadata_table_name = get_column_metadata_table_name_for_table(table_name)
    column_metadata = ColumnMetadata(column_metadata_as_list)
    properties = Properties(
        table_name,
        openapi_spec.get_definition(table_name),
        openapi_spec,
        column_metadata,
        column_metadata_table_name=column_metadata_table_name
    )
    # Built once and reused below: as_dict() makes new metadata on every call, so
    # choices and widgets set on one call's result would never reach the form.
    properties_as_dict = properties.as_dict()
    for property_name, metadata in properties_as_dict.items():
        metadata.widget = widget_for(table_name, property_name)
        choices = choices_for(table_name, property_name, choices_context)
        if choices:
            metadata.choices = choices
    possible_fk_table_column_name = f'{column_metadata_table_name}_id'
    definitions_by_table_name = dict()
    if infer_one_to_many_properties:
        references_to_table = openapi_spec.find_references_to_table(
            table_name,
            possible_column_name=possible_fk_table_column_name
        )
        references_to_table.pop(table_name, None)
        definitions_by_table_name = {
            table_name: openapi_spec.get_definition(table_name)
            for table_name in references_to_table.keys()
        }
    one_to_many_properties = OneToManyProperties(
        table_name,
        definitions_by_table_name,
        openapi_spec,
        column_metadata,
        column_metadata_table_name=column_metadata_table_name
    )
    return FormConfig(
        properties_as_dict,
        one_to_many_properties=one_to_many_properties.as_dict(),
        additional_disabled_properties=disabled_properties
    )
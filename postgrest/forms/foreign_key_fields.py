import lxml.html
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from .form_config import FormConfig, PropertiesMetadata

from editor.forms.base_forms import ForeignKeyFormWithDynamicallyPopulatedFields
from editor.services import prepare_initial_form_data
from postgrest.api_clients import ApiClient
from resource_management.forms import ResourceDeletionForm


def get_foreign_key_form_configs(
        table_names: list[str],
        openapi_spec: dict,
        column_metadata: list[dict]
    ) -> dict[str, FormConfig]:
    """Gets the form configs for each foreign key
    field in a definition.

    Args:
        table_names (list[str]): The names of the
        tables for the foreign key fields.
        openapi_spec (dict): The OpenAPI 2.0 spec to
        pass to the PropertiesMetadata class.
        column_metadata (list[dict]): The list of
        records from the column_metadata table to pass
        to the PropertiesMetadata class.

    Returns:
        dict: Key-value pairs of each foreign key field's
        table's mapped to their FormConfig instance.
    """
    # table_names are the same as definition names
    # (each definition corresponds to a table
    # and vice versa).
    form_configs = {}
    for table_name in table_names:
        properties_metadata = PropertiesMetadata(
            table_name,
            openapi_spec,
            column_metadata,
        ).as_dict()
        form_configs.update({
            table_name: FormConfig(properties_metadata),
        })
    return form_configs


def get_new_one_to_one_field_forms(
        form_config: FormConfig
    ) -> dict[str, ForeignKeyFormWithDynamicallyPopulatedFields]:
    return ForeignKeyFormWithDynamicallyPopulatedFields(
        form_config.get_fields(),
        id_prefix='new'
    )


def get_one_to_one_field_update_form(
        resource_id: int,
        table_name: str,
        form_config: FormConfig
    ) -> ForeignKeyFormWithDynamicallyPopulatedFields:
    return  ForeignKeyFormWithDynamicallyPopulatedFields(
        form_config.get_fields(),
        id_suffix=f'{table_name}_{resource_id}',
        initial=form_config.initial
    )


def get_one_to_one_field_forms(
        resource: dict,
        form_configs: dict[str, FormConfig],
        categorised_field_names: dict[str, list]
    ) -> dict[str, dict]:
    """Generates separate forms for one-to-one foreign key
    fields (as these are sent separately from the main editor
    form).

    Args:
        resource (dict): The resource that has the one-to-one field(s).
        form_configs (list[FormConfig]): The form configs
        for each one-to-one field's table.
        categorised_field_names (dict[str, list]): A dict mapping that
        maps one-to-one fields to their tables.

    Returns:
        dict[str, dict]:
        A dict mapping each one-to-one field to relevant forms and
        terminology.
    """
    one_to_one_field_metadata = {}
    for fk_table_name, form_config in form_configs.items():
        property_names = categorised_field_names.get(fk_table_name, list())
        fk_api_client = ApiClient.get_client_instance_by_endpoint(fk_table_name)
        for property_name in property_names:
            initial = dict()
            fk_resource_id = None
            try:
                fk_resource_id = resource.get(property_name)
            except AttributeError:
                pass
            if fk_resource_id:
                fk_resource = fk_api_client.get(fk_resource_id)
                initial = prepare_initial_form_data(fk_resource)
            one_to_one_field_metadata.update({
                property_name: {
                    "new_form": ForeignKeyFormWithDynamicallyPopulatedFields(
                        form_config.get_fields(),
                        id_prefix=f'new_{property_name}'
                    ),
                    "update_form": ForeignKeyFormWithDynamicallyPopulatedFields(
                        form_config.get_fields(),
                        id_suffix=f"{property_name}",
                        initial=initial,
                    ),
                    "delete_form": ResourceDeletionForm(
                        initial={"resource_id_to_delete": fk_resource_id}
                    ),
                    "type_readable": fk_api_client.type_readable,
                    "type_readable_plural": fk_api_client.type_readable_plural,
                },
            })
    return one_to_one_field_metadata


def get_one_to_many_field_forms(
    request,
    resource_id: int,
    form_configs: dict[str, FormConfig],
    update_one_to_many_relation_reverse_base: str,
    delete_one_to_many_relation_reverse_base: str
) -> dict[str, dict]:
    # Table names become the field names in the main form.
    one_to_many_field_metadata = {}
    for table_name, form_config in form_configs.items():
        fk_api_client = ApiClient.get_client_instance_by_endpoint(table_name)
        if not fk_api_client:
            continue
        fk_resources = fk_api_client.get_resources_referencing_resource_id(
            'capacity_id', resource_id,
        )
        pk_field_name = fk_api_client.endpoint_definition.pk_field_name
        one_to_many_field_metadata.update({
            table_name: {
                "new_form": ForeignKeyFormWithDynamicallyPopulatedFields(
                    form_config.get_fields(),
                    id_prefix=f'new_{table_name}'
                ),
                "resource_forms": {
                    fk_resource.get(pk_field_name): {
                        "update_form": ForeignKeyFormWithDynamicallyPopulatedFields(
                            form_config.get_fields(),
                            id_suffix=f"{table_name}_{pk_field_name}",
                            initial=prepare_initial_form_data(fk_resource),
                        ),
                        "delete_form": ResourceDeletionForm(
                            initial={
                                "resource_id_to_delete": fk_resource.get(pk_field_name)
                            }
                        ),
                    }
                    for fk_resource in fk_resources
                },
                "type_readable": fk_api_client.type_readable,
                "type_readable_plural": fk_api_client.type_readable_plural,
                "templates": {
                    "update_dialog": render_to_string(
                        "editor/dialogs/update_dialog.html",
                        {
                            "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                                form_config.get_fields(),
                                id_suffix="__resource_id__",
                            ),
                            "resource_id": "__resource_id__",
                            "update_resource_url": reverse_lazy(
                                update_one_to_many_relation_reverse_base,
                                kwargs={
                                    "resource_id": resource_id,
                                    "fk_column_name": table_name,
                                    "fk_resource_id": "__resource_id__",
                                },
                            ),
                            "dialog_id": f"update-{table_name}-__resource_id__-dialog",
                            "dialog_extra_classes": "col-lg-10",
                            "resource_type_readable": fk_api_client.endpoint,
                        },
                        request=request
                    ),
                    "delete_dialog": render_to_string(
                        "editor/dialogs/delete_dialog.html",
                        {
                            "form": ResourceDeletionForm(
                                initial={
                                    "resource_id_to_delete": "__resource_id__"
                                }
                            ),
                            "resource_id": "__resource_id__",
                            "delete_resource_url": reverse_lazy(
                                delete_one_to_many_relation_reverse_base,
                                kwargs={
                                    "resource_id": resource_id,
                                    "fk_column_name": table_name,
                                    "fk_resource_id": "__resource_id__",
                                },
                            ),
                            "dialog_id": f"delete-{table_name}-__resource_id__-dialog",
                            "dialog_extra_classes": "col-lg-10",
                            "resource_type_readable": fk_api_client.endpoint,
                        },
                        request=request
                    ),
                    "list_item": render_to_string(
                        "editor/foreign_key_fields/one_to_many_field_list_item.html",
                        {
                            "form": ForeignKeyFormWithDynamicallyPopulatedFields(
                                form_config.get_fields(),
                                id_suffix="__resource_id__",
                            ),
                            "resource_id": "__resource_id__",
                            "resource_type_readable": fk_api_client.endpoint,
                            "field": {"name": table_name},
                        },
                        request=request
                    ),
                },
            },
        })
    return one_to_many_field_metadata
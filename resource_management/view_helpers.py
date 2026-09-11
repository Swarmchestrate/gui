from collections import OrderedDict

from postgrest.api import OpenApiSpecification, Resource
from postgrest.forms.form_config import FormConfig
from postgrest.table_names import TableNames


DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT = [
    # Column metadata for "APPLICATION_NEW" is stored in "APPLICATION".
    TableNames.APPLICATION_NEW,
    # Column metadata for "CAPACITY_NEW" is stored in "CAPACITY".
    TableNames.CAPACITY_NEW,
    "geography_columns",
    "geometry_columns",
    "spatial_ref_sys",
]


def get_composite_pk(resource: Resource):
    return f"{resource.as_dict().get('table_name')}__{resource.as_dict().get('column_name')}"


def get_postgrest_table_names(openapi_spec: OpenApiSpecification) -> list:
    return [
        table_name
        for table_name in openapi_spec.get_definitions().keys()
        if table_name not in DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT
    ]


def _get_field_data_by_category_for_table_name(
        table_name: str,
        column_metadata: list[Resource]) -> dict[str, dict]:
    if table_name in DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT:
        return dict()
    UNCATEGORISED = "Unknown"
    column_metadata_by_category = {
        UNCATEGORISED: dict(),
    }
    DEFAULT_ORDER_NUMBER = 999999
    for resource in column_metadata:
        cm_table_name = resource.as_dict().get("table_name", "")
        if cm_table_name != table_name:
            continue
        category = resource.as_dict().get("category", "")
        title = resource.as_dict().get(
            "title",
            resource.as_dict().get("column_name")
        )
        order_number = resource.as_dict().get("order", DEFAULT_ORDER_NUMBER)
        if not isinstance(order_number, int):
            order_number = DEFAULT_ORDER_NUMBER
        field_data = {
            "title": title,
            "order": order_number,
        }
        if not category or len(category.strip()) == 0:
            column_metadata_by_category[UNCATEGORISED].update({
                get_composite_pk(resource): field_data,
            })
            continue
        if category not in column_metadata_by_category:
            column_metadata_by_category.update({
                category: dict(),
            })
        column_metadata_by_category[category].update({
            get_composite_pk(resource): field_data,
        })
    return column_metadata_by_category


def get_ordered_fields_and_categories_for_table_name(
        table_name: str,
        form_config: FormConfig,
        openapi_spec: OpenApiSpecification,
        column_metadata_by_id: dict[str, Resource]) -> dict:
    postgrest_table_names = get_postgrest_table_names(openapi_spec)
    if (table_name not in postgrest_table_names
        or table_name in DISABLED_TABLE_NAMES_IN_COLUMN_METADATA_MANAGEMENT):
        return dict()
    
    data = dict()
    DEFAULT_ORDER_NUMBER = 999999

    field_order_by_category = _get_field_data_by_category_for_table_name(
        table_name,
        list(column_metadata_by_id.values())
    )
    # Format the dict to a list to make sorting easier.
    category_order = [
        {
            "category": category_name,
            "order": max(
                field_order.values(),
                key=lambda data: data.get("order", DEFAULT_ORDER_NUMBER),
                default={"order": DEFAULT_ORDER_NUMBER}
            ).get("order")
        }
        for category_name, field_order in field_order_by_category.items()
    ]
    data = {
        order_data["category"]: field_order_by_category.get(
            order_data["category"],
            dict()
        )
        for order_data in sorted(
            category_order,
            key=lambda order_data: order_data["order"]
        )
    }

    UNCATEGORISED = "Unknown"
    # The column metadata table uses the "table_name" column and the "column_name"
    # column to form a composite PK. These should be included so they can be specified
    # in the UI.
    include_pk_fields = (table_name == "column_metadata")
    fields_names = form_config.get_fields(include_pk_fields=include_pk_fields).keys()
    # Go through each field and ensure it has an order number, so they all appear
    # in the right order in the UI.
    for field_name in fields_names:
        # These dict keys should match the stringified composite key
        # format of the column metadata records ({table_name}__{column_name}).
        possible_resource_pk = f"{table_name}__{field_name}"
        # Assign a default order number to fields without column metadata,
        # otherwise, skip.
        if possible_resource_pk in column_metadata_by_id:
            continue
        data[UNCATEGORISED].update({
            # This should mirror the "field_data" dict in
            # _get_field_data_by_category_for_table_name().
            possible_resource_pk: {
                "order": DEFAULT_ORDER_NUMBER,
                "title": field_name,
            }
        })

    for category_name, category_field_data in data.items():
        data.update({
            category_name: {
                field_pk: field_data
                for field_pk, field_data in sorted(
                    list(category_field_data.items()),
                    key=lambda item: item[1].get("order")
                )
            }
        })

    return data


def get_update_data_for_new_field_order(
        current_category_and_field_order: dict[str, dict],
        table_name: str,
        column_name: str,
        new_category_name: str):
    updated_order = OrderedDict()
    update_data = list()
    # Ensure an existing entry doesn't exist in the current category/field
    # order to prevent possibility of duplicates.
    for category_name, fields in current_category_and_field_order.items():
        if category_name not in updated_order:
            updated_order.update({category_name: list()})
        for field_pk in fields.keys():
            if field_pk == f"{table_name}__{column_name}":
                continue
            updated_order[category_name].append(field_pk)
    if new_category_name not in updated_order:
        updated_order.update({
            new_category_name: list(),
        })
    # This key for this new dict entry should mirror the get_composite_pk()
    # output.
    updated_order[new_category_name].append(
        f"{table_name}__{column_name}"
    )
    order_num_counter = 0
    for category_name, field_pks in updated_order.items():
        for field_pk in field_pks:
            f_table_name, f_column_name = field_pk.split("__")
            update_data.append({
                "table_name": f_table_name,
                "column_name": f_column_name,
                "category": category_name,
                "order": order_num_counter,
            })
            order_num_counter += 1
    return update_data
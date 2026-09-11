from postgrest.api import Resource
from postgrest.forms.form_config import FormConfig


def get_composite_pk(resource: Resource):
    return f"{resource.as_dict().get('table_name')}__{resource.as_dict().get('column_name')}"


def _get_field_data_by_category_for_table_name(
        table_name: str,
        column_metadata: list[Resource],
        disabled_table_names: list[str] = None) -> dict[str, dict]:
    if not disabled_table_names:
        disabled_table_names = list()
    if table_name in disabled_table_names:
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
        column_metadata_by_id: dict[str, Resource],
        postgrest_table_names: list[str],
        disabled_table_names: list[str] = None) -> dict:
    if not disabled_table_names:
        disabled_table_names = list()
    if (table_name not in postgrest_table_names
        or table_name in disabled_table_names):
        return dict()
    
    data = dict()
    DEFAULT_ORDER_NUMBER = 999999

    field_order_by_category = _get_field_data_by_category_for_table_name(
        table_name,
        list(column_metadata_by_id.values()),
        disabled_table_names=disabled_table_names
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
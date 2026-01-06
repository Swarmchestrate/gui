from postgrest.base.base_api_clients import ApiClient

from .utils import UNCATEGORISED_CATEGORY

# from postgrest.mocks.base.mock_base_api_clients import MockApiClient as ApiClient


def _add_category_descendents(
    category: str,
    category_data: dict,
    category_names: list[str],
    parent_category: str = "",
):
    processed_categories = set()
    if category in processed_categories:
        return
    processed_categories.add(category)
    if category not in category_data:
        category_data.update(
            {
                category: {
                    "title": category,
                    "non_toc_title": category.replace(":", ": "),
                    "descendents": dict(),
                },
            }
        )
        if parent_category:
            category_data[category].update(
                {
                    "title": category.replace(f"{parent_category}:", ""),
                }
            )

    category_with_colon = f"{category}:"
    descendent_names = [
        possible_descendent_name
        for possible_descendent_name in category_names
        if (
            category in possible_descendent_name
            and category != possible_descendent_name
            and ":" not in possible_descendent_name.replace(category_with_colon, "")
        )
    ]
    for dn in descendent_names:
        _add_category_descendents(
            dn,
            category_data[category]["descendents"],
            category_names,
            parent_category=category,
        )


def get_categories_for_editor(
    api_client: ApiClient, column_metadata: list[dict]
) -> dict:
    category_names = list(set(r.get("category", "") for r in column_metadata))
    category_names.sort()

    categories = dict()
    for category in category_names:
        _add_category_descendents(category, categories, category_names)

    categorised_field_names = set(
        cm.get("column_name", "") for cm in column_metadata if cm.get("column_name", "")
    )
    user_specifiable_field_names = set(
        api_client.endpoint_definition.get_all_user_specifiable_fields().keys()
    )
    uncategorised_property_names = (
        user_specifiable_field_names - categorised_field_names
    )
    if uncategorised_property_names:
        category_names.append(UNCATEGORISED_CATEGORY)
        categories.update(
            {
                UNCATEGORISED_CATEGORY: {
                    "title": UNCATEGORISED_CATEGORY,
                    "non_toc_title": UNCATEGORISED_CATEGORY,
                    "descendents": dict(),
                }
            }
        )
    return categories

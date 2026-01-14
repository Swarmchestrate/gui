from postgrest.base.base_api_clients import ApiClient

# from postgrest.mocks.base.mock_base_api_clients import MockApiClient as ApiClient
from .utils import UNCATEGORISED_CATEGORY


def _add_metadata_for_category(
    category: str,
    category_names: list[str],
    categories_with_metadata: dict,
    processed_categories: set,
):
    if category in processed_categories:
        return
    processed_categories.add(category)
    if category in categories_with_metadata:
        return
    # Previous & next categories
    current_category_index = category_names.index(category)
    prev_category = None
    if not current_category_index == 0:
        prev_category = category_names[current_category_index - 1]
    next_category = None
    if not (current_category_index == (len(category_names) - 1)):
        next_category = category_names[current_category_index + 1]
    # Category metadata
    categories_with_metadata.update(
        {
            category: {
                "title": category,
                "non_toc_title": category.replace(":", ": "),
                "descendents": dict(),
                "previous": prev_category,
                "next": next_category,
            },
        }
    )


def _add_descendents_for_category(
    category: str,
    category_names: list[str],
    categories_with_metadata: dict,
    processed_categories: set[str],
    descendent_categories: set[str],
    parent_category: str = "",
):
    if category in processed_categories:
        return
    processed_categories.add(category)
    # Remove parent category from title displayed
    # in TOC.
    if parent_category:
        categories_with_metadata[category].update(
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
            and ":"
            not in possible_descendent_name.replace(
                category_with_colon, ""
            )  # Checks if "direct" descendent.
        )
    ]
    descendent_categories.update(descendent_names)
    for dn in descendent_names:
        _add_descendents_for_category(
            dn,
            category_names,
            categories_with_metadata,
            processed_categories,
            descendent_categories,
            parent_category=category,
        )
        categories_with_metadata[category]["descendents"].update(
            {dn: categories_with_metadata.get(dn, {})}
        )


def get_categories_for_editor(
    api_client: ApiClient, column_metadata: list[dict], category_names: list[str]
) -> dict:
    categories = dict()
    processed_categories = set()
    # Add metadata for each category
    for category in category_names:
        _add_metadata_for_category(
            category, category_names, categories, processed_categories
        )

    # Check if an "uncategorised" category
    # is needed before sorting categories
    # into descendents.
    categorised_field_names = set(
        cm.get("column_name", "") for cm in column_metadata if cm.get("column_name", "")
    )
    user_specifiable_field_names = set(
        api_client.endpoint_definition.get_all_user_specifiable_fields().keys()
    )
    uncategorised_property_names = (
        user_specifiable_field_names - categorised_field_names
    )
    uncategorised_metadata = {}
    if uncategorised_property_names:
        last_category = category_names[-1]
        categories[last_category].update({"next": UNCATEGORISED_CATEGORY})
        uncategorised_metadata = {
            "title": UNCATEGORISED_CATEGORY,
            "non_toc_title": UNCATEGORISED_CATEGORY,
            "descendents": dict(),
            "previous": last_category,
            "next": None,
        }

    # Sort categories under descendents
    descendent_categories = set()
    processed_categories_ = set()
    for category in category_names:
        _add_descendents_for_category(
            category,
            category_names,
            categories,
            processed_categories_,
            descendent_categories,
        )
    for descendent_category in descendent_categories:
        categories.pop(descendent_category)
    # Add uncategorised metadata last to avoid potential
    # confusion.
    if uncategorised_property_names:
        categories.update({UNCATEGORISED_CATEGORY: uncategorised_metadata})
        category_names.append(UNCATEGORISED_CATEGORY)
    return categories

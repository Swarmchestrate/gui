from postgrest.forms.form_config import (
    ColumnMetadata,
    FormConfig,
    Properties,
    OneToManyProperties,
)
from postgrest.api import OpenApiSpecification, Resource
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY


class EditorTableOfContents:
    def __init__(
            self,
            table_name: str,
            category_names: list[str],
            is_unknown_category_needed: bool = False):
        self.table_name = table_name
        self.category_names = category_names
        self.is_unknown_category_needed = is_unknown_category_needed

    def _add_metadata_for_category(
            self,
            category: str,
            table_of_contents: dict,
            processed_categories: set):
        if category in processed_categories:
            return
        processed_categories.add(category)
        if category in table_of_contents:
            return
        # Previous & next categories
        current_category_index = self.category_names.index(category)
        prev_category = None
        if not current_category_index == 0:
            prev_category = self.category_names[current_category_index - 1]
        next_category = None
        if not (current_category_index == (len(self.category_names) - 1)):
            next_category = self.category_names[current_category_index + 1]
        # Category metadata
        table_of_contents.update({
            category: {
                "title": category,
                "non_toc_title": category.replace(":", ": "),
                "descendents": dict(),
                "previous": prev_category,
                "next": next_category,
            },
        })

    def _add_descendents_for_category(
            self,
            category: str,
            table_of_contents: dict,
            processed_categories: set[str],
            descendent_categories: set[str],
            parent_category: str = ""):
        if category in processed_categories:
            return
        processed_categories.add(category)
        # Remove parent category from title displayed
        # in TOC.
        if parent_category:
            table_of_contents[category].update(
                {
                    "title": category.replace(f"{parent_category}:", ""),
                }
            )
        category_with_colon = f"{category}:"
        descendent_names = [
            possible_descendent_name
            for possible_descendent_name in self.category_names
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
            self._add_descendents_for_category(
                dn,
                table_of_contents,
                processed_categories,
                descendent_categories,
                parent_category=category,
            )
            table_of_contents[category]["descendents"].update(
                {dn: table_of_contents.get(dn, {})}
            )

    def as_dict(self) -> dict:
        """Sorts a list of categories into hierarchical order as
        a dict. If any properties don't have a category (found by
        comparing the definition properties with the column metadata
        properties) then an "Uncategorised" category is added.

        Returns:
            dict: Returns a dict representation of the table of contents
            ready to use with an editor.
        """
        table_of_contents = dict()
        processed_categories = set()
        # Add metadata for each category
        for category in self.category_names:
            self._add_metadata_for_category(
                category,
                table_of_contents,
                processed_categories
            )

        # Check if an "uncategorised" category is needed before sorting
        # categories into descendents, as it will be harder to set
        # the "next" property of the current last category when it's
        # nested.
        uncategorised_metadata = {}
        if (self.is_unknown_category_needed):
            last_category = self.category_names[-1]
            table_of_contents[last_category].update({"next": UNKNOWN_ATTRIBUTE_CATEGORY})
            uncategorised_metadata = {
                "title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "non_toc_title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "descendents": dict(),
                "previous": last_category,
                "next": None,
            }

        # Sort categories in hierarchical order
        descendent_categories = set()
        processed_categories = set()
        for category in self.category_names:
            self._add_descendents_for_category(
                category,
                table_of_contents,
                processed_categories,
                descendent_categories,
            )
        for descendent_category in descendent_categories:
            table_of_contents.pop(descendent_category)
        
        # The "uncategorised" category is added last to
        # avoid potential confusion with real categories.
        if (self.is_unknown_category_needed):
            table_of_contents.update({UNKNOWN_ATTRIBUTE_CATEGORY: uncategorised_metadata})
            # self.category_names.append(UNKNOWN_ATTRIBUTE_CATEGORY)
        return table_of_contents


def get_form_config_for_table(
        table_name: str,
        openapi_spec: OpenApiSpecification,
        column_metadata_as_list: list[Resource],
        infer_one_to_many_properties: bool = True,
        column_metadata_table_name: str = None,
        disabled_categories: list[str] = None,
        disabled_properties: list[str] = None) -> FormConfig:
    if not column_metadata_table_name:
        column_metadata_table_name = table_name
    if not disabled_categories:
        disabled_categories = list()
    if not disabled_properties:
        disabled_properties = list()
    column_metadata = ColumnMetadata(column_metadata_as_list)
    properties = Properties(
        table_name,
        openapi_spec.get_definition(table_name),
        openapi_spec,
        column_metadata,
        column_metadata_table_name=column_metadata_table_name
    )
    properties_as_dict = {
        property_name: metadata
        for property_name, metadata in properties.as_dict().items()
        if metadata.category not in disabled_categories
    }
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
        column_metadata,
        column_metadata_table_name=column_metadata_table_name
    )
    return FormConfig(
        properties_as_dict,
        one_to_many_properties=one_to_many_properties.as_dict(),
        extra_disabled_properties=disabled_properties
    )

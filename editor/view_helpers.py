from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY


class EditorTableOfContents:
    def __init__(
            self,
            table_name: str,
            category_names: list[str],
            column_metadata: list[dict],
            definition_properties: list[str],
            disabled_categories: list[str] = None):
        self.table_name = table_name
        self.category_names = category_names
        self.column_metadata = column_metadata
        self.definition_properties = definition_properties
        self.disabled_categories = list()
        if disabled_categories:
            self.disabled_categories = disabled_categories

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

        # Check if an "uncategorised" category
        # is needed before sorting categories
        # into descendents.

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
        
        # Check if an "uncategorised" category is needed. It's
        # added last to avoid potential confusion with real
        # categories.
        properties_with_category = set(
            cm.get("column_name", "")
            for cm in self.column_metadata
            if cm.get("column_name", "")
        )
        uncategorised_property_names = self.definition_properties - properties_with_category
        uncategorised_metadata = {}
        if uncategorised_property_names:
            last_category = self.category_names[-1]
            table_of_contents[last_category].update({"next": UNKNOWN_ATTRIBUTE_CATEGORY})
            uncategorised_metadata = {
                "title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "non_toc_title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "descendents": dict(),
                "previous": last_category,
                "next": None,
            }
            table_of_contents.update({UNKNOWN_ATTRIBUTE_CATEGORY: uncategorised_metadata})
            self.category_names.append(UNKNOWN_ATTRIBUTE_CATEGORY)
        return table_of_contents

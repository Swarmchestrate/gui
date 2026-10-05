from collections import OrderedDict
from django.forms import Field

from postgrest.api import Resource
from postgrest.forms.form_config import FormConfig
from postgrest.view_helpers import (
    ForeignKeyTableFormConfigViewMixin,
    FormConfigViewMixin,
)
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.helpers import get_column_metadata_table_name_for_table


class EditorTableOfContents:
    def __init__(
            self,
            table_name: str,
            category_names: list[str],
            is_unknown_category_needed: bool = False):
        self.table_name = table_name
        self.category_names = [
            category_name
            for category_name in category_names
            if (category_name is not None
                and not len(category_name.strip()) == 0)
        ]
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
                # Parent categories are removed from the descendent "title"
                # later. E.g., "parent:descendent" -> "descendent".
                "title": category,
                # The "full_title" keeps the parent categories from the original
                # category text - the colons separating the categories just have
                # a space added to make the full title more readable.
                # E.g., "parent:descendent" -> "parent: descendent".
                "full_title": category.replace(":", ": "),
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
            table_of_contents[category].update({
                "title": category.replace(f"{parent_category}:", ""),
            })
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

        # Check if an "uncategorised" category is needed before sorting
        # categories into descendents, as it will be harder to set
        # the "next" property of the current last category when it's
        # nested.
        uncategorised_metadata = {}
        if self.is_unknown_category_needed:
            uncategorised_metadata = {
                "title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "full_title": UNKNOWN_ATTRIBUTE_CATEGORY,
                "descendents": dict(),
                "previous": None,
                "next": None,
            }
        last_category = None
        try:
            last_category = self.category_names[-1]
        except IndexError:
            pass
        if (not last_category and len(self.category_names) == 1):
            self.category_names = []
            last_category = None
        
        # Add metadata for each category
        for category in self.category_names:
            self._add_metadata_for_category(
                category,
                table_of_contents,
                processed_categories
            )
        if (last_category
            and not len(self.category_names) == 1
            and self.is_unknown_category_needed):
            table_of_contents[last_category].update({"next": UNKNOWN_ATTRIBUTE_CATEGORY})
            uncategorised_metadata.update({
                "previous": last_category,
            })

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


class EditorViewMixin(FormConfigViewMixin):
    _fields_for_toc_generation: list[Field]

    def _is_column_metadata_resource_fit_for_toc(self, resource: Resource) -> bool:
        return resource.as_dict().get(
            "table_name",
            ""
        ) == get_column_metadata_table_name_for_table(self.table_name)

    def get_toc_list_items(self) -> dict:
        form_config = self.get_form_config()
        self._fields_for_toc_generation = form_config.get_fields()
        return get_toc_list_items_for_table(
            self.table_name,
            form_config,
            **self.get_toc_kwargs()
        )

    def get_toc_kwargs(self) -> dict:
        return {
            "is_unknown_category_needed": any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in self._fields_for_toc_generation.values()
            )
        }


class ForeignKeyEditorViewMixin(ForeignKeyTableFormConfigViewMixin, EditorViewMixin):
    _fk_table_fields_for_toc_generation: list[Field]

    def _is_column_metadata_resource_fit_for_fk_table_toc(self, resource: Resource) -> bool:
        return resource.as_dict().get(
            "table_name",
            ""
        ) == get_column_metadata_table_name_for_table(self.fk_table_name)

    def get_fk_table_toc_list_items(self) -> dict:
        fk_table_form_config = self.get_fk_table_form_config()
        self._fk_table_fields_for_toc_generation = fk_table_form_config.get_fields()
        return get_toc_list_items_for_table(
            self.fk_table_name,
            fk_table_form_config,
            **self.get_fk_table_toc_kwargs()
        )

    def get_fk_table_toc_kwargs(self) -> dict:
        return {
            "is_unknown_category_needed": any(
                field.category == UNKNOWN_ATTRIBUTE_CATEGORY
                for field in self._fk_table_fields_for_toc_generation.values()
            )
        }


def get_toc_list_items_for_table(
        table_name: str,
        form_config: FormConfig,
        is_unknown_category_needed: bool = True):
    DEFAULT_ORDER_NUMBER = 999999
    category_names = list(OrderedDict.fromkeys(
        field.metadata.category
        for field in sorted(
            form_config.get_fields().values(),
            key=lambda field: (
                field.metadata.order
                if field.metadata.order is not None
                else DEFAULT_ORDER_NUMBER
            )
        )
    ).keys())
    return EditorTableOfContents(
        table_name,
        category_names,
        is_unknown_category_needed=is_unknown_category_needed
    ).as_dict()
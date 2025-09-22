from django.views.generic import TemplateView

from .api_endpoint_client import (
    ApiEndpointClient,
    ColumnMetadataApiEndpointClient
)


class EditorView(TemplateView):
    registration_type_name_singular: str
    registration_type_name_plural: str
    api_endpoint_client: ApiEndpointClient
    id_field: str

    editor_registration_list_url_reverse: str
    editor_start_url_reverse_base: str
    editor_url_reverse_base: str
    editor_overview_url_reverse_base: str

    api_endpoint_client_class: ApiEndpointClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_endpoint_client = self.api_endpoint_client_class()
        self.id_field = self.api_endpoint_client.endpoint_definition.id_field

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'description': self.api_endpoint_client.endpoint_definition.description,
            'registration_type_name_singular': self.registration_type_name_singular,
            'registration_type_name_plural': self.registration_type_name_plural,
            'editor_registration_list_url_reverse': self.editor_registration_list_url_reverse,
            'editor_url_reverse_base': self.editor_url_reverse_base,
            'editor_start_url_reverse_base': self.editor_start_url_reverse_base,
            'editor_overview_url_reverse_base': self.editor_overview_url_reverse_base,
            'id_field': self.id_field,
        })
        return context


class EditorTocView(TemplateView):
    column_metadata_api_endpoint_client_class: ColumnMetadataApiEndpointClient
    categories: dict
    column_metadata: list[dict]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.column_metadata_api_endpoint_client = self.column_metadata_api_endpoint_client_class()
        self._setup_column_metadata()
        self._setup_categories()

    def _setup_column_metadata(self):
        self.column_metadata = self.column_metadata_api_endpoint_client.get_registrations()

    def _setup_categories(self):
        self.category_names = list(set(
            r.get('category')
            for r in self.column_metadata
        ))
        self.category_names.sort()
        processed_categories = set()

        def add_category_descendents(category: str, category_data: dict, parent_category: str = ''):
            if category in processed_categories:
                return
            processed_categories.add(category)
            if category not in category_data:
                category_data.update({
                    category: {
                        'title': category,
                        'non_toc_title': category.replace(':', ': '),
                        'descendents': dict(),
                    },
                })
                if parent_category:
                    category_data[category].update({
                        'title': category.replace(f'{parent_category}:', ''),
                    })

            category_with_colon = f'{category}:'
            descendent_names = [
                possible_descendent_name
                for possible_descendent_name in self.category_names
                if (category in possible_descendent_name
                    and category != possible_descendent_name
                    and ':' not in possible_descendent_name.replace(category_with_colon, '')
                )
            ]
            for dn in descendent_names:
                add_category_descendents(
                    dn,
                    category_data[category]['descendents'],
                    parent_category=category
                )

        self.categories = dict()
        for category in self.category_names:
            add_category_descendents(
                category,
                self.categories
            )

    def _get_first_category(self):
        return next(iter(self.category_names))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'toc_list_items': self.categories,
        })
        return context

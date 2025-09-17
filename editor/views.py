import json
import urllib.parse
from http import HTTPStatus

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from .api_endpoint_client import ApiEndpointClient, ColumnMetadataApiEndpointClient
from .forms import RegistrationsListForm


class EditorView(View):
    registration_type_name_singular: str
    registration_type_name_plural: str
    api_endpoint_client: ApiEndpointClient
    id_field: str

    editor_registration_list_url_reverse: str
    editor_start_url_reverse_base: str
    editor_url_reverse_base: str

    api_endpoint_client_class: ApiEndpointClient
    column_metadata_api_endpoint_client_class: ColumnMetadataApiEndpointClient
    categories: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_endpoint_client = self.api_endpoint_client_class()
        self.column_metadata_api_endpoint_client = self.column_metadata_api_endpoint_client_class()
        self.id_field = self.api_endpoint_client.endpoint_definition.id_field
        self._setup_categories()

    def _setup_categories(self):
        self.category_names = list(set(
            r.get('category')
            for r in self.column_metadata_api_endpoint_client.get_registrations(params={
                'select': 'category',
            })
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
                        'descendents': dict(),
                    },
                })
                if parent_category:
                    category_data.update({
                        category: {
                            'title': category.replace(f'{parent_category}:', ''),
                        },
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
            'description': self.api_endpoint_client.endpoint_definition.description,
            'registration_type_name_singular': self.registration_type_name_singular,
            'registration_type_name_plural': self.registration_type_name_plural,
            'editor_registration_list_url_reverse': self.editor_registration_list_url_reverse,
            'editor_url_reverse_base': self.editor_url_reverse_base,
            'editor_start_url_reverse_base': self.editor_start_url_reverse_base,
            'id_field': self.id_field,
            'toc_list_items': self.categories,
        })
        return context



class EditorStartFormView(EditorView, FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'New {self.registration_type_name_singular.title()}',
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_endpoint_client': self.api_endpoint_client,
            'column_metadata_api_endpoint_client': self.column_metadata_api_endpoint_client,
        })
        return kwargs

    def form_valid(self, form):
        new_registration = self.api_endpoint_client.register(form.cleaned_data)
        messages.success(self.request, f'New {self.api_endpoint_client.endpoint_definition.definition_name} registered.')
        self.success_url = reverse_lazy(
            self.editor_url_reverse_base,
            kwargs={
                'registration_id': new_registration.get(self.id_field),
            }
        )
        return super().form_valid(form)


class EditorFormView(EditorView, FormView):
    title_base = ''

    def get_prev_and_next_list_items(self):
        index_of_current_category = self.category_names.index(self.category)
        prev_list_item = ''
        try:
            if index_of_current_category == 0:
                raise IndexError
            prev_list_item = self.category_names[index_of_current_category - 1]
        except IndexError:
            pass

        next_list_item = ''
        try:
            next_list_item = self.category_names[index_of_current_category + 1]
        except IndexError:
            pass

        return (prev_list_item, next_list_item)

    def dispatch(self, request, *args, **kwargs):
        self.registration_id = self.kwargs['registration_id']
        self.category = self.request.GET.get(
            'category',
            self._get_first_category()
        )
        self.success_url = self.request.path
        self.title_base = f'{self.registration_type_name_singular.title()} {self.registration_id}'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        prev_list_item, next_list_item = self.get_prev_and_next_list_items()
        context = super().get_context_data(**kwargs)
        category_formatted = self.category.replace(':', ': ')
        context.update({
            'title': f'{self.title_base} | {category_formatted}',
            'main_subheading': self.registration_type_name_singular.title(),
            'main_heading': category_formatted,
            'current_category': self.category,
            'prev_list_item': prev_list_item,
            'prev_list_item_title': prev_list_item.replace(':', ': '),
            'next_list_item': next_list_item,
            'next_list_item_title': next_list_item.replace(':', ': '),
            'registration_id': self.registration_id,
        })
        return context


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        registration_data = self.api_endpoint_client.get(self.registration_id)
        kwargs.update({
            'api_endpoint_client': self.api_endpoint_client,
            'column_metadata_api_endpoint_client': self.column_metadata_api_endpoint_client,
            'category': self.category,
            'initial': registration_data,
        })
        return kwargs

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            messages.error(self.request, 'Some fields were invalid. Please see feedback below.')
            return response
        return JsonResponse({
            'feedback': json.loads(form.errors.as_json()),
            'url': self.request.path,
        }, status=HTTPStatus.BAD_REQUEST)

    def form_valid(self, form):
        prev_list_item, next_list_item = self.get_prev_and_next_list_items()
        if next_list_item:
            self.success_url = '%s?category=%s' % (
                reverse_lazy(
                    self.editor_url_reverse_base,
                    kwargs={
                        'registration_id': self.registration_id,
                    }
                ),
                urllib.parse.quote_plus(next_list_item)
            )
        response = super().form_valid(form)
        self.api_endpoint_client.update(
            self.registration_id,
            form.cleaned_data
        )
        message = f'Updated {self.category}'
        if self.request.accepts('text/html'):
            messages.success(self.request, message)
            return response
        return JsonResponse({
            'message': message,
            'redirect': self.success_url,
        })


class RegistrationsListFormView(EditorView, FormView):
    template_name = 'editor/registrations_list.html'
    form_class = RegistrationsListForm

    new_registration_reverse: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registrations_list = self.api_endpoint_client.get_registrations()

    def dispatch(self, request, *args, **kwargs):
        self.success_url = request.path
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.registration_type_name_plural.title(),
            'registrations': {
                registration.get(self.id_field): registration
                for registration in self.registrations_list
            },
            'new_registration_reverse': self.new_registration_reverse,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'registration_ids': [
                registration.get(self.id_field)
                for registration in self.registrations_list
            ]
        })
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred whilst deleting registrations. The registrations may not have been deleted.')
        return super().form_invalid(form)

    def form_valid(self, form):
        registration_ids_to_delete = form.cleaned_data.get('registration_ids_to_delete', [])
        self.api_endpoint_client.delete_many(registration_ids_to_delete)
        messages.success(self.request, f'Deleted {len(registration_ids_to_delete)} registrations')
        return super().form_valid(form)

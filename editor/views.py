import json
from http import HTTPStatus

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from .api_endpoint_client import ApiEndpointClient


class EditorView(View):
    registration_type_name_singular: str
    registration_type_name_plural: str
    api_endpoint_client: ApiEndpointClient

    editor_start_url_reverse_base: str
    editor_url_reverse_base: str

    title_base = ''
    api_endpoint_client_class = ApiEndpointClient

    def _get_first_field_format(self):
        return next(iter(
            self.api_endpoint_client_class()
            .endpoint_definition
            .get_user_specifiable_field_formats()
        ))

    def dispatch(self, request, *args, **kwargs):
        self.api_endpoint_client = self.api_endpoint_client_class()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'description': self.api_endpoint_client.endpoint_definition.description,
            'registration_type_name_singular': self.registration_type_name_singular,
            'registration_type_name_plural': self.registration_type_name_plural,
            'editor_url_reverse_base': self.editor_url_reverse_base,
            'editor_start_url_reverse_base': self.editor_start_url_reverse_base,
            'id_field': self.api_endpoint_client.endpoint_definition.id_field,
            'toc_list_items': (self.api_endpoint_client_class()
                                .endpoint_definition
                                .get_user_specifiable_field_formats()),
        })
        return context
    


class EditorStartFormView(EditorView, FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title_base,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_endpoint_client': self.api_endpoint_client_class(),
        })
        return kwargs

    def form_valid(self, form):
        new_registration = self.api_endpoint_client.register(form.cleaned_data)
        messages.success(self.request, f'New {self.api_endpoint_client.endpoint_definition.definition_name} registered.')
        self.success_url = reverse_lazy(
            self.editor_url_reverse_base,
            kwargs={
                'registration_id': new_registration.get(self.api_endpoint_client.endpoint_definition.id_field),
            }
        )
        return super().form_valid(form)


class EditorFormView(EditorView, FormView):
    def get_prev_and_next_list_items(self):
        field_formats = (self.api_endpoint_client_class()
                        .endpoint_definition
                        .get_user_specifiable_field_formats())
        index_of_current_field_format = field_formats.index(self.field_format)
        prev_list_item = None
        try:
            if index_of_current_field_format == 0:
                raise IndexError
            prev_list_item = field_formats[index_of_current_field_format - 1]
        except IndexError:
            pass

        next_list_item = None
        try:
            next_list_item = field_formats[index_of_current_field_format + 1]
        except IndexError:
            pass

        return (prev_list_item, next_list_item)

    def dispatch(self, request, *args, **kwargs):
        self.registration_id = self.kwargs['registration_id']
        self.field_format = self.request.GET.get(
            'format',
            self._get_first_field_format()
        )
        self.success_url = self.request.path
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        prev_list_item, next_list_item = self.get_prev_and_next_list_items()
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.title_base} | {self.field_format}',
            'main_subheading': self.title_base,
            'main_heading': self.field_format,
            'current_field_format': self.field_format,
            'prev_list_item': prev_list_item,
            'next_list_item': next_list_item,
            'registration_id': self.registration_id,
        })
        return context
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_endpoint_client': self.api_endpoint_client_class(),
            'field_format': self.field_format,
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
            self.success_url = '%s?format=%s' % (
                reverse_lazy(
                    self.editor_url_reverse_base,
                    kwargs={
                        'registration_id': self.registration_id,
                    }
                ),
                next_list_item
            )
        response = super().form_valid(form)
        self.api_endpoint_client.update(
            self.registration_id,
            form.cleaned_data
        )
        message = f'Updated {self.field_format}'
        if self.request.accepts('text/html'):
            messages.success(self.request, message)
            return response
        return JsonResponse({
            'message': message,
            'redirect': self.success_url,
        })


class RegistrationsTemplateView(EditorView, TemplateView):
    template_name = 'editor/registrations_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('self.api_endpoint_client', self.api_endpoint_client)
        print('self.api_endpoint_client.get_registrations()', self.api_endpoint_client.get_registrations())
        context.update({
            'title': self.registration_type_name_plural.title(),
            'registrations': self.api_endpoint_client.get_registrations()
        })
        return context
    
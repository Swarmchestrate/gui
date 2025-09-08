import json
from http import HTTPStatus

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .api_endpoint_client import ApiEndpointClient


class EditorView(View):
    api_endpoint_client: ApiEndpointClient

    title_base = ''
    api_endpoint_client_class = ApiEndpointClient
    
    def _get_editor_url_reverse_base(self):
        app_name = self.request.resolver_match.app_name
        url_name = self.request.resolver_match.url_name
        if not app_name:
            return url_name
        return f'{app_name}:{url_name}'

    def dispatch(self, request, *args, **kwargs):
        self.editor_url_reverse_base = self._get_editor_url_reverse_base()
        self.api_endpoint_client = self.api_endpoint_client_class()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'editor_url_reverse_base': self.editor_url_reverse_base,
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
            self._get_editor_url_reverse_base(),
            kwargs={
                'id': new_registration.get(self.api_endpoint_client.endpoint_definition.id_field),
                'field_format': next(iter(
                    self.api_endpoint_client_class()
                    .endpoint_definition
                    .get_user_specifiable_field_formats()
                ))
            }
        )
        return super().form_valid(form)


class EditorFormView(EditorView, FormView):
    def dispatch(self, request, *args, **kwargs):
        self.registration_id = self.kwargs['id']
        self.field_format = self.kwargs['field_format']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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
        if self.request.GET.get('response_format') == 'json':
            return JsonResponse(
                {
                    'feedback': json.loads(form.errors.as_json()),
                    'url': self.request.path,
                },
                status=HTTPStatus.BAD_REQUEST
            )
        return super().form_invalid(form)
    
    def form_valid(self, form):
        return super().form_valid(form)
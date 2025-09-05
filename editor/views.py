import json
from http import HTTPStatus

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .api_endpoint_client import ApiEndpointClient


class EditorView(View):
    title_base = ''
    api_endpoint_client_class = ApiEndpointClient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'toc_list_items': self.api_endpoint_client_class().endpoint_definition.get_user_specifiable_field_formats(),
        })
        return context
    


class EditorStartFormView(EditorView, FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title_base,
            'start_url': reverse_lazy(
                self.request.resolver_match.url_name,
                kwargs={
                    'field_format': next(iter(
                        self.api_endpoint_client_class().endpoint_definition.get_user_specifiable_field_formats()
                    ))
                }
            ),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_endpoint_client': self.api_endpoint_client_class(),
        })
        return kwargs


class EditorFormView(EditorView, FormView):
    def dispatch(self, request, *args, **kwargs):
        self.field_format = self.kwargs['field_format']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        field_formats = self.api_endpoint_client_class().endpoint_definition.get_user_specifiable_field_formats()
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
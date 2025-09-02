import json
from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import FormView

from .api_client import ApiClient


class EditorFormView(FormView):
    api_client_class = ApiClient

    def dispatch(self, request, *args, **kwargs):
        try:
            self.field_format = self.kwargs['field_format']
        except KeyError:
            first_field_format = next(iter(self.api_client_class().get_field_formats()))
            return redirect(self.request.resolver_match.view_name, first_field_format)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'toc_list_items': self.api_client_class().get_field_formats()
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_client': self.api_client_class(),
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
    
import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic import FormView


class EditorFormView(FormView):
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
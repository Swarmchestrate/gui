from django.urls import reverse_lazy

from .forms import (
    NewCloudCapacityForm,
    NewEdgeCapacityForm,
)
from editor.views import EditorFormView


class CloudCapacityEditorFormView(EditorFormView):
    template_name = 'capacities/new_cloud_capacity.html'
    form_class = NewCloudCapacityForm
    success_url = reverse_lazy('new_cloud_capacity')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Cloud Capacity',
        }) 
        return context


class EdgeCapacityEditorFormView(EditorFormView):
    template_name = 'capacities/new_edge_capacity.html'
    form_class = NewEdgeCapacityForm
    success_url = reverse_lazy('new_edge_capacity')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Edge Capacity',
        }) 
        return context

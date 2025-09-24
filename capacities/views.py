from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic import FormView

from .api_endpoint_client import (
    CloudCapacityApiEndpointClient,
    CloudCapacityColumnMetadataApiEndpointClient,
    EdgeCapacityApiEndpointClient,
    EdgeCapacityColumnMetadataApiEndpointClient,
)
from .forms import (
    CapacityPriceEditorForm,
    CloudCapacityRegistrationForm,
    CloudCapacityEditorForm,
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)

from editor.views import (
    EditorView,
    EditorProcessFormView,
    EditorOverviewTemplateView,
    EditorRouterView,
    EditorStartFormView,
    RegistrationsListFormView,
)


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = 'capacities:cloud_capacities_list'
    editor_url_reverse_base = 'capacities:cloud_capacity_editor'
    editor_start_url_reverse_base = 'capacities:new_cloud_capacity'
    editor_overview_url_reverse_base = 'capacities:cloud_capacity_overview'
    registration_type_name_singular = 'cloud capacity'
    registration_type_name_plural = 'cloud capacities'
    api_endpoint_client_class = CloudCapacityApiEndpointClient
    column_metadata_api_endpoint_client_class = CloudCapacityColumnMetadataApiEndpointClient


class CloudCapacityEditorStartFormView(CloudCapacityEditorView, EditorStartFormView, FormView):
    template_name = 'capacities/new_cloud_capacity_start.html'
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorProcessFormView(CloudCapacityEditorView, EditorProcessFormView):
    template_name = 'capacities/capacity_editor.html'
    form_class = CloudCapacityEditorForm
    success_url = reverse_lazy('capacities:new_cloud_capacity')


class CloudCapacityEditorRouterView(CloudCapacityEditorView, EditorRouterView):
    editor_view_class = CloudCapacityEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == 'cost & locality':
            return CloudCapacityCostAndLocalityEditorTemplateView.as_view()(request, *args, **kwargs)
        return super().route_to_view(request, *args, **kwargs)


class CloudCapacityCostAndLocalityEditorTemplateView(CloudCapacityEditorProcessFormView):
    PriceFormset = formset_factory(CapacityPriceEditorForm)

    def add_formset_data_to_main_form(self, cleaned_data: dict, forms: dict):
        cleaned_data = super().add_formset_data_to_main_form(cleaned_data, forms)
        price_formset = forms.get('price')
        price_unformatted = price_formset.cleaned_data
        price_formatted = dict()
        for price_data in price_unformatted:
            if not price_data:
                continue
            price_formatted.update({
                price_data.get('price_instance_type', ''): '%s credit/hour' % (
                    price_data.get('price_credits_per_hour')
                )
            })
        if price_formatted:
            cleaned_data.update({
                'price': price_formatted,
            })
        return cleaned_data

    def get_context_data_forms_invalid(self, forms):
        context = super().get_context_data_forms_invalid(forms)
        context.update({
            'price_formset': forms.get('price'),
        })
        return context

    def get_forms_from_request_data(self, request):
        forms = super().get_forms_from_request_data(request)
        price_formset = self.PriceFormset(request.POST)
        forms.update({
            'price': price_formset,
        })
        return forms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = list()
        for instance_type, credits_per_hour in self.registration.get('price').items():
            credits_per_hour_num = int(credits_per_hour.replace(' credit/hour', ''))
            initial.append({
                'price_instance_type': instance_type,
                'price_credits_per_hour': credits_per_hour_num,
            })
        price_formset = self.PriceFormset(initial=initial)
        context.update({
            'price_formset': price_formset,
        })
        return context


class CloudCapacityRegistrationsListFormView(CloudCapacityEditorView, RegistrationsListFormView):
    new_registration_reverse = 'capacities:new_cloud_capacity'


class CloudCapacityEditorOverviewTemplateView(CloudCapacityEditorView, EditorOverviewTemplateView):
    pass


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = 'capacities:edge_capacities_list'
    editor_url_reverse_base = 'capacities:edge_capacity_editor'
    editor_start_url_reverse_base = 'capacities:new_edge_capacity'
    editor_overview_url_reverse_base = 'capacities:edge_capacity_overview'
    registration_type_name_singular = 'edge capacity'
    registration_type_name_plural = 'edge capacities'
    title_base = 'New Edge Capacity'
    api_endpoint_client_class = EdgeCapacityApiEndpointClient
    column_metadata_api_endpoint_client_class = EdgeCapacityColumnMetadataApiEndpointClient


class EdgeCapacityEditorStartFormView(EdgeCapacityEditorView, EditorStartFormView):
    template_name = 'capacities/new_edge_capacity_start.html'
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorProcessFormView(EdgeCapacityEditorView, EditorProcessFormView):
    template_name = 'capacities/capacity_editor.html'
    form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy('capacities:new_edge_capacity')


class EdgeCapacityRegistrationsListFormView(EdgeCapacityEditorView, RegistrationsListFormView):
    new_registration_reverse = 'capacities:new_edge_capacity'


class EdgeCapacityEditorOverviewTemplateView(EdgeCapacityEditorView, EditorOverviewTemplateView):
    pass

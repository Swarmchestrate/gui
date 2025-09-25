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
    CapacityEnergyConsumptionEditorForm,
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


# Cloud & Edge Capacities
class CapacityEditorRouterView(EditorRouterView):
    cost_and_locality_editor_view_class = None
    energy_editor_view_class = None

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == 'cost & locality':
            return self.cost_and_locality_editor_view_class.as_view()(request, *args, **kwargs)
        elif self.category.lower() == 'energy':
            return self.energy_editor_view_class.as_view()(request, *args, **kwargs)
        return super().route_to_view(request, *args, **kwargs)


class CapacityCostAndLocalityEditorProcessFormView(EditorProcessFormView):
    PriceFormset = formset_factory(CapacityPriceEditorForm)

    formset_context_varname = 'price_formset'
    price_formset_prefix = 'price'
    price_property_name = 'price'

    def add_formset_data_to_main_form(self, cleaned_data: dict, forms: dict):
        cleaned_data = super().add_formset_data_to_main_form(cleaned_data, forms)
        price_formset = forms.get(self.price_formset_prefix)
        price_unformatted = price_formset.cleaned_data
        price_formatted = dict()
        for data in price_unformatted:
            if not data:
                continue
            price_formatted.update({
                data.get('instance_type'): '%s credit/hour' % (
                    data.get('credits_per_hour')
                )
            })
        if price_formatted:
            cleaned_data.update({
                self.price_property_name: price_formatted,
            })
        return cleaned_data

    def get_context_data_forms_invalid(self, forms):
        context = super().get_context_data_forms_invalid(forms)
        context.update({
            self.formset_context_varname: forms.get(self.price_formset_prefix),
        })
        return context

    def get_forms_from_request_data(self, request):
        forms = super().get_forms_from_request_data(request)
        price_formset = self.PriceFormset(
            request.POST,
            prefix=self.price_formset_prefix
        )
        forms.update({
            self.price_formset_prefix: price_formset,
        })
        return forms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = list()
        for instance_type, credits_per_hour in self.registration.get(self.price_property_name).items():
            credits_per_hour_num = int(credits_per_hour.replace(' credit/hour', ''))
            initial.append({
                'instance_type': instance_type,
                'credits_per_hour': credits_per_hour_num,
            })
        price_formset = self.PriceFormset(
            initial=initial,
            prefix=self.price_formset_prefix
        )
        context.update({
            self.formset_context_varname: price_formset,
        })
        return context


class CapacityEnergyEditorProcessFormView(EditorProcessFormView):
    EnergyConsumptionFormset = formset_factory(CapacityEnergyConsumptionEditorForm)

    formset_context_varname = 'energy_consumption_formset'
    energy_consumption_formset_prefix = 'energy_consumption'
    energy_consumption_property_name = 'energy_consumption'

    def add_formset_data_to_main_form(self, cleaned_data: dict, forms: dict):
        cleaned_data = super().add_formset_data_to_main_form(cleaned_data, forms)
        energy_consumption_formset = forms.get(self.energy_consumption_formset_prefix)
        energy_consumption_unformatted = energy_consumption_formset.cleaned_data
        energy_consumption_formatted = dict()
        for data in energy_consumption_unformatted:
            if not data:
                continue
            energy_consumption_formatted.update({
                data.get('type'): data.get('amount'),
            })
        if energy_consumption_formatted:
            cleaned_data.update({
                self.energy_consumption_property_name: energy_consumption_formatted,
            })
        return cleaned_data

    def get_context_data_forms_invalid(self, forms):
        context = super().get_context_data_forms_invalid(forms)
        context.update({
            self.formset_context_varname: forms.get(self.energy_consumption_formset_prefix),
        })
        return context

    def get_forms_from_request_data(self, request):
        forms = super().get_forms_from_request_data(request)
        energy_consumption_formset = self.EnergyConsumptionFormset(
            request.POST,
            prefix=self.energy_consumption_formset_prefix
        )
        forms.update({
            self.energy_consumption_formset_prefix: energy_consumption_formset,
        })
        return forms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = list()
        energy_consumption_data = self.registration.get(self.energy_consumption_property_name)
        if not energy_consumption_data:
            energy_consumption_data = dict()
        for type, amount in energy_consumption_data.items():
            initial.append({
                'type': type,
                'amount': amount,
            })
        energy_consumption_formset = self.EnergyConsumptionFormset(
            initial=initial,
            prefix=self.energy_consumption_formset_prefix
        )
        context.update({
            self.formset_context_varname: energy_consumption_formset,
        })
        return context


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


class CloudCapacityCostAndLocalityEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        CapacityCostAndLocalityEditorProcessFormView):
    pass


class CloudCapacityEnergyEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        CapacityEnergyEditorProcessFormView):
    pass


class CloudCapacityEditorRouterView(CloudCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = CloudCapacityEditorProcessFormView
    cost_and_locality_editor_view_class = CloudCapacityCostAndLocalityEditorProcessFormView
    energy_editor_view_class = CloudCapacityEnergyEditorProcessFormView


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

import geonamescache
from http import HTTPStatus

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .api_endpoint_client import (
    CloudCapacityApiEndpointClient,
    CloudCapacityColumnMetadataApiEndpointClient,
    EdgeCapacityApiEndpointClient,
    EdgeCapacityColumnMetadataApiEndpointClient,
)
from .forms import (
    CapacityEnergyConsumptionEditorForm,
    CapacityLocalityEditorForm,
    CapacityLocalitySearchForm,
    CapacityPriceEditorForm,
    CapacitySecurityPortsEditorForm,
    CloudCapacityRegistrationForm,
    CloudCapacityEditorForm,
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)
from .formsets import (
    CapacityEnergyConsumptionEditorFormSet,
    CapacityLocalityEditorFormSet,
    CapacityPriceEditorFormSet,
    CapacitySecurityPortsEditorFormSet,
)
from .view_mixins import (
    AccessibleSensorsFormsetEditorViewMixin,
    ArchitectureFormSetEditorViewMixin,
    DevicesFormsetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
)

from editor.views import (
    EditorView,
    EditorProcessFormView,
    EditorOverviewTemplateView,
    EditorRouterView,
    EditorStartFormView,
    MultipleEditorFormsetProcessFormView,
    RegistrationsListFormView,
)


# Cloud & Edge Capacities
class CapacityEditorRouterView(EditorRouterView):
    cost_and_locality_editor_view_class = None
    energy_editor_view_class = None
    security_trust_and_access_editor_view_class = None

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == 'cost & locality':
            return self.cost_and_locality_editor_view_class.as_view()(request, *args, **kwargs)
        elif self.category.lower() == 'energy':
            return self.energy_editor_view_class.as_view()(request, *args, **kwargs)
        elif self.category.lower() == 'security, trust & access':
            return self.security_trust_and_access_editor_view_class.as_view()(request, *args, **kwargs)
        return super().route_to_view(request, *args, **kwargs)


class CapacityCostAndLocalityEditorProcessFormView(MultipleEditorFormsetProcessFormView):
    def dispatch(self, request, *args, **kwargs):
        # Price
        price_property_name = 'price'
        self.add_formset_class(
            CapacityPriceEditorForm,
            price_property_name,
            base_formset_class=CapacityPriceEditorFormSet
        )

        # Configure initial formset data
        initial_price = list()
        price_data = self.registration.get(price_property_name)
        if not price_data:
            price_data = dict()
        for instance_type, credits_per_hour in price_data.items():
            credits_per_hour_num = float(credits_per_hour.replace(
                ' credit/hour',
                ''
            ))
            initial_price.append({
                'instance_type': instance_type,
                'credits_per_hour': credits_per_hour_num,
            })
        self.add_initial_data_for_formset(initial_price, price_property_name)

        # Locality
        locality_property_name = 'locality'
        self.add_formset_class(
            CapacityLocalityEditorForm,
            locality_property_name,
            base_formset_class=CapacityLocalityEditorFormSet,
            can_delete=False,
            extra_formset_factory_kwargs={
                'extra': 0,
                'max_num': 1,
            }
        )

        # Configure initial formset data
        initial_locality = list()
        locality_data = self.registration.get(locality_property_name)
        if (not locality_data
            or not isinstance(locality_data, dict)):
            locality_data = {
                'continent': '',
                'country': '',
                'city': '',
                'gps': '',
            }
        initial_locality.append(locality_data)
        self.add_initial_data_for_formset(initial_locality, locality_property_name)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'locality_search_form': CapacityLocalitySearchForm(prefix='locality'),
            'locality_search_form_url_reverse': reverse_lazy('capacities:locality_search'),
        })
        return context


class CapacityLocalitySearchFormView(TemplateView):
    template_name = 'editor/editor_base.html'

    def get(self, request, *args, **kwargs):
        form = CapacityLocalitySearchForm(data=request.GET)
        if (not form.is_valid()):
            return JsonResponse({}, status_code=HTTPStatus.BAD_REQUEST)
        query = form.cleaned_data.get('query', '')
        gc = geonamescache.GeonamesCache()
        options = list()
        all_continents = gc.get_continents()
        continents = {
            continent_code: {
                'name': continent.get('toponymName'),
                'optgroup': 'continents',
            }
            for continent_code, continent in all_continents.items()
            if query.lower() in continent.get('toponymName').lower()
        }
        options += continents.values()
        all_country_names = gc.get_countries_by_names()
        countries = [
            {
                'name': country_name,
                'optgroup': 'countries',
            }
            for country_name in all_country_names
            if query.lower() in country_name.lower()
        ]
        options += countries
        cities = gc.search_cities(query)
        cities = [
            {
                'name': city.get('name'),
                'optgroup': 'cities',
            }
            for city in cities
        ]
        options += cities
        return JsonResponse({
            'options': options,
        })


class CapacityEnergyEditorProcessFormView(MultipleEditorFormsetProcessFormView):
    def dispatch(self, request, *args, **kwargs):
        property_name = 'energy_consumption'
        self.add_formset_class(
            CapacityEnergyConsumptionEditorForm,
            property_name,
            base_formset_class=CapacityEnergyConsumptionEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        energy_consumption_data = self.registration.get(property_name)
        if not energy_consumption_data:
            energy_consumption_data = dict()
        for type, amount in energy_consumption_data.items():
            initial.append({
                'type': type,
                'amount': amount,
            })
        self.add_initial_data_for_formset(initial, property_name)
        return super().dispatch(request, *args, **kwargs)


class CapacitySecurityTrustAndAccessEditorProcessFormView(
        MultipleEditorFormsetProcessFormView):
    def dispatch(self, request, *args, **kwargs):
        property_name = 'security_ports'
        self.add_formset_class(
            CapacitySecurityPortsEditorForm,
            property_name,
            base_formset_class=CapacitySecurityPortsEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        security_ports = self.registration.get(property_name)
        if not security_ports:
            security_ports = list()
        for port_number in security_ports:
            initial.append({
                'port_number': int(port_number),
            })
        self.add_initial_data_for_formset(initial, property_name)
        return super().dispatch(request, *args, **kwargs)


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
    main_form_class = CloudCapacityEditorForm
    success_url = reverse_lazy('capacities:new_cloud_capacity')


class CloudCapacityCostAndLocalityEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        CapacityCostAndLocalityEditorProcessFormView):
    pass


class CloudCapacityEnergyEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        CapacityEnergyEditorProcessFormView):
    pass


class CloudCapacitySecurityTrustAndAccessEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        CapacitySecurityTrustAndAccessEditorProcessFormView):
    pass


class CloudCapacitySystemSpecificEditorProcessFormView(
        CloudCapacityEditorProcessFormView,
        MultipleEditorFormsetProcessFormView,
        ArchitectureFormSetEditorViewMixin,
        OperatingSystemFormSetEditorViewMixin):
    def dispatch(self, request, *args, **kwargs):
        self.add_architecture_formset_metadata()
        self.add_operating_system_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityEditorRouterView(CloudCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = CloudCapacityEditorProcessFormView
    cost_and_locality_editor_view_class = CloudCapacityCostAndLocalityEditorProcessFormView
    energy_editor_view_class = CloudCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = CloudCapacitySecurityTrustAndAccessEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == 'system specific':
            return CloudCapacitySystemSpecificEditorProcessFormView.as_view()(request, *args, **kwargs)
        return super().route_to_view(request, *args, **kwargs)


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
    main_form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy('capacities:new_edge_capacity')


class EdgeCapacityCostAndLocalityEditorProcessFormView(
        EdgeCapacityEditorProcessFormView,
        CapacityCostAndLocalityEditorProcessFormView):
    pass


class EdgeCapacityEnergyEditorProcessFormView(
        EdgeCapacityEditorProcessFormView,
        CapacityEnergyEditorProcessFormView):
    pass


class EdgeCapacitySpecificEditorProcessFormView(
        EdgeCapacityEditorProcessFormView,
        MultipleEditorFormsetProcessFormView,
        AccessibleSensorsFormsetEditorViewMixin,
        DevicesFormsetEditorViewMixin):
    def dispatch(self, request, *args, **kwargs):
        self.add_accessible_sensors_formset_metadata()
        self.add_devices_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacitySecurityTrustAndAccessEditorProcessFormView(
        EdgeCapacityEditorProcessFormView,
        CapacitySecurityTrustAndAccessEditorProcessFormView):
    pass


class EdgeCapacityEditorRouterView(EdgeCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = EdgeCapacityEditorProcessFormView
    cost_and_locality_editor_view_class = EdgeCapacityCostAndLocalityEditorProcessFormView
    energy_editor_view_class = EdgeCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = EdgeCapacitySecurityTrustAndAccessEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == 'edge specific':
            return EdgeCapacitySpecificEditorProcessFormView.as_view()(request, *args, **kwargs)
        return super().route_to_view(request, *args, **kwargs)


class EdgeCapacityRegistrationsListFormView(EdgeCapacityEditorView, RegistrationsListFormView):
    new_registration_reverse = 'capacities:new_edge_capacity'


class EdgeCapacityEditorOverviewTemplateView(EdgeCapacityEditorView, EditorOverviewTemplateView):
    pass

from http import HTTPStatus

import geonamescache
import reverse_geocode
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import ProcessFormView

from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorRouterView,
    EditorStartFormView,
    EditorView,
    MultipleEditorFormsetProcessFormView,
    RegistrationsListFormView,
)
from instance_types.forms import InstanceTypeEditorForm
from instance_types.formsets import InstanceTypeFormSet

# from instance_types.api_endpoint_client import InstanceTypeApiEndpointClient
from instance_types.mocks.api_endpoint_client import InstanceTypeApiEndpointClient

# from .api_endpoint_client import (
#     CloudCapacityApiEndpointClient,
#     CloudCapacityColumnMetadataApiEndpointClient,
#     EdgeCapacityApiEndpointClient,
#     EdgeCapacityColumnMetadataApiEndpointClient,
# )
from .forms import (
    CapacityEnergyConsumptionEditorForm,
    CapacityGetLocalityByGpsForm,
    CapacityGetLocalityByNameForm,
    CapacityLocalityOptionsSearchForm,
    CapacityPriceEditorForm,
    CapacitySecurityPortsEditorForm,
    CloudCapacityEditorForm,
    CloudCapacityRegistrationForm,
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)
from .formsets import (
    CapacityEnergyConsumptionEditorFormSet,
    CapacityPriceEditorFormSet,
    CapacitySecurityPortsEditorFormSet,
)
from .mixins.view_mixins import (
    AccessibleSensorsFormsetEditorViewMixin,
    ArchitectureFormSetEditorViewMixin,
    DevicesFormsetEditorViewMixin,
    LocalityFormSetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
)
from .mocks.api_endpoint_client import (
    CloudCapacityApiEndpointClient,
    CloudCapacityColumnMetadataApiEndpointClient,
    EdgeCapacityApiEndpointClient,
    EdgeCapacityColumnMetadataApiEndpointClient,
)


# Cloud & Edge Capacities
class CapacityEditorRouterView(EditorRouterView):
    metadata_editor_view_class = None
    specs_editor_view_class = None
    cost_and_locality_editor_view_class = None
    energy_editor_view_class = None
    security_trust_and_access_editor_view_class = None

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "metadata":
            return self.metadata_editor_view_class.as_view()(request, *args, **kwargs)
        if self.category.lower() == "specs":
            return self.specs_editor_view_class.as_view()(request, *args, **kwargs)
        elif self.category.lower() == "cost & locality":
            return self.cost_and_locality_editor_view_class.as_view()(
                request, *args, **kwargs
            )
        elif self.category.lower() == "energy":
            return self.energy_editor_view_class.as_view()(request, *args, **kwargs)
        elif self.category.lower() == "security":
            return self.security_trust_and_access_editor_view_class.as_view()(
                request, *args, **kwargs
            )
        return super().route_to_view(request, *args, **kwargs)


class CapacityMetadataEditorProcessFormView(
    LocalityFormSetEditorViewMixin, MultipleEditorFormsetProcessFormView
):
    def dispatch(self, request, *args, **kwargs):
        self.add_locality_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class CapacityCostAndLocalityEditorProcessFormView(
    MultipleEditorFormsetProcessFormView
):
    def dispatch(self, request, *args, **kwargs):
        # Price
        price_property_name = "price"
        self.add_formset_class(
            CapacityPriceEditorForm,
            price_property_name,
            base_formset_class=CapacityPriceEditorFormSet,
        )

        # Configure initial formset data
        initial_price = list()
        price_data = self.registration.get(price_property_name)
        if not price_data:
            price_data = dict()
        for instance_type, credits_per_hour in price_data.items():
            credits_per_hour_num = float(credits_per_hour.replace(" credit/hour", ""))
            initial_price.append(
                {
                    "instance_type": instance_type,
                    "credits_per_hour": credits_per_hour_num,
                }
            )
        self.add_initial_data_for_formset(initial_price, price_property_name)

        return super().dispatch(request, *args, **kwargs)


class CapacityLocalityOptionsSearchProcessFormView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        form = CapacityLocalityOptionsSearchForm(data=request.GET)
        if not form.is_valid():
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
        query = form.cleaned_data.get("query", "")
        options = list()
        gc = geonamescache.GeonamesCache()
        all_continents = gc.get_continents()
        continents = {
            continent_code: {
                "name": continent.get("name"),
                "optgroup": "continents",
                "value": f"continent_{continent.get('geonameId')}_{continent_code}",
            }
            for continent_code, continent in all_continents.items()
            if query.lower() in continent.get("toponymName").lower()
        }
        options += continents.values()
        all_countries = gc.get_countries()
        countries = [
            {
                "name": country.get("name"),
                "optgroup": "countries",
                "value": f"country_{country.get('geonameid')}_{country_code}",
            }
            for country_code, country in all_countries.items()
            if query.lower() in country.get("name", "").lower()
        ]
        options += countries
        cities = gc.search_cities(query)
        cities = [
            {
                "name": city.get("name"),
                "country_name": all_countries.get(city.get("countrycode", ""), {}).get(
                    "name"
                ),
                "optgroup": "cities",
                "value": f"city_{city.get('geonameid')}_{city.get('name')}",
            }
            for city in cities
        ]
        options += cities
        return JsonResponse(
            {
                "options": options,
            }
        )


class CapacityGetLocalityProcessFormView(ProcessFormView):
    def get_city(
        self,
        gc: geonamescache.GeonamesCache,
        geoname_id: int | None,
        selected_city_name: str,
    ) -> dict:
        cities = gc.get_cities()
        city = next(
            (
                city
                for city_code, city in cities.items()
                if int(city_code) == int(geoname_id)
            ),
            dict(),
        )
        return city

    def get_country(
        self, gc: geonamescache.GeonamesCache, selected_country_code: str
    ) -> dict:
        all_countries = gc.get_countries()
        country = next(
            (
                country
                for country_code, country in all_countries.items()
                if selected_country_code == country_code
            ),
            dict(),
        )
        return country

    def get_continent(
        self, gc: geonamescache.GeonamesCache, selected_continent_code: str
    ) -> dict:
        all_continents = gc.get_continents()
        continent = next(
            (
                continent
                for continent_code, continent in all_continents.items()
                if selected_continent_code == continent_code
            ),
            dict(),
        )
        return continent

    def get(self, request, *args, **kwargs):
        return JsonResponse({})


class CapacityGetLocalityByNameProcessFormView(CapacityGetLocalityProcessFormView):
    def get(self, request, *args, **kwargs):
        locality = {
            "continent": "",
            "country": "",
            "city": "",
        }
        form = CapacityGetLocalityByNameForm(data=request.GET)
        if not form.is_valid():
            return JsonResponse(
                {"errors": form.errors.as_json()}, status=HTTPStatus.BAD_REQUEST
            )
        geoname_id = form.cleaned_data.get("geoname_id")
        selected_continent_code = form.cleaned_data.get("continent_code")
        selected_country_code = form.cleaned_data.get("country_code")
        selected_city_name = form.cleaned_data.get("city_name")
        gc = geonamescache.GeonamesCache()
        if selected_city_name:
            city = self.get_city(gc, geoname_id, selected_city_name)
            locality.update(
                {
                    "city": city.get("name", ""),
                }
            )
            selected_country_code = city.get("countrycode")
        if selected_country_code:
            country = self.get_country(gc, selected_country_code)
            locality.update(
                {
                    "country": country.get("name", ""),
                }
            )
            selected_continent_code = country.get("continentcode")
        if selected_continent_code:
            continent = self.get_continent(gc, selected_continent_code)
            locality.update(
                {
                    "continent": continent.get("name", ""),
                }
            )
        return JsonResponse(locality)


class CapacityGetLocalityByGpsProcessFormView(CapacityGetLocalityProcessFormView):
    def get_nearest_known_location(
        self, gps_location: tuple[float, float] | None
    ) -> dict:
        """Returns a dict containing data (including city and
        country) on the nearest known location to the provided
        coordinates.
        """
        if not gps_location or gps_location[0] is None or gps_location[1] is None:
            return dict()
        return reverse_geocode.get(gps_location)

    def get(self, request, *args, **kwargs):
        locality = {
            "continent": "",
            "country": "",
            "city": "",
        }
        form = CapacityGetLocalityByGpsForm(data=request.GET)
        if not form.is_valid():
            return JsonResponse(
                {"errors": form.errors.as_json()}, status=HTTPStatus.BAD_REQUEST
            )
        gps_location = form.cleaned_data.get("gps_location")
        nearest_known_location = self.get_nearest_known_location(gps_location)
        locality.update(
            {
                "city": nearest_known_location.get("city", ""),
                "country": nearest_known_location.get("country", ""),
            }
        )
        selected_country_code = nearest_known_location.get("country_code")
        selected_continent_code = None
        gc = geonamescache.GeonamesCache()
        if selected_country_code:
            country = self.get_country(gc, selected_country_code)
            locality.update(
                {
                    "country": country.get("name", ""),
                }
            )
            selected_continent_code = country.get("continentcode")
        if selected_continent_code:
            continent = self.get_continent(gc, selected_continent_code)
            locality.update(
                {
                    "continent": continent.get("name", ""),
                }
            )
        return JsonResponse(locality)


class CapacityEnergyEditorProcessFormView(MultipleEditorFormsetProcessFormView):
    def dispatch(self, request, *args, **kwargs):
        property_name = "energy_consumption"
        self.add_formset_class(
            CapacityEnergyConsumptionEditorForm,
            property_name,
            base_formset_class=CapacityEnergyConsumptionEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        energy_consumption_data = self.registration.get(property_name)
        if not energy_consumption_data:
            energy_consumption_data = dict()
        for type, amount in energy_consumption_data.items():
            initial.append(
                {
                    "type": type,
                    "amount": amount,
                }
            )
        self.add_initial_data_for_formset(initial, property_name)
        return super().dispatch(request, *args, **kwargs)


class CapacitySecurityTrustAndAccessEditorProcessFormView(
    MultipleEditorFormsetProcessFormView
):
    def dispatch(self, request, *args, **kwargs):
        property_name = "security_ports"
        self.add_formset_class(
            CapacitySecurityPortsEditorForm,
            property_name,
            base_formset_class=CapacitySecurityPortsEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        security_ports = self.registration.get(property_name)
        if not security_ports:
            security_ports = list()
        for port_number in security_ports:
            initial.append(
                {
                    "port_number": int(port_number),
                }
            )
        self.add_initial_data_for_formset(initial, property_name)
        return super().dispatch(request, *args, **kwargs)


class CapacitySpecsEditorProcessFormView(MultipleEditorFormsetProcessFormView):
    manually_processed_formsets: dict

    def process_instance_types(
        self,
        formset: InstanceTypeFormSet,
        api_endpoint_client_class: InstanceTypeApiEndpointClient,
    ):
        instance_type_api_client = api_endpoint_client_class()
        inst_type_id_field_name = instance_type_api_client.endpoint_definition.id_field
        current_instance_type_id_strs = list(
            map(str, self.registration.get("instance_types"))
        )
        instance_types_to_add = list()
        instance_types_to_update = list()
        instance_type_ids_to_delete = set()
        updated_instance_types_data = formset.to_api_ready_format()
        for instance_type in updated_instance_types_data:
            instance_type_id = instance_type.get(inst_type_id_field_name)
            if instance_type_id is None:
                instance_types_to_add.append(instance_type)
                continue
            if str(instance_type_id) not in current_instance_type_id_strs:
                instance_type_ids_to_delete.add(instance_type_id)
                continue
            instance_types_to_update.append(instance_type)
        # New instance types
        new_instance_type_ids = list()
        if instance_types_to_add:
            new_instance_type_ids = instance_type_api_client.bulk_register(
                instance_types_to_add
            )
        # Updating instance types
        updated_instance_type_ids = list()
        if instance_types_to_update:
            for instance_type in instance_types_to_update:
                instance_type_id = instance_type.get(inst_type_id_field_name)
                updated_instance_type_ids.append(instance_type_id)
                instance_type.pop(inst_type_id_field_name)
                instance_type_api_client.update(instance_type_id, instance_type)
        # Deleting instance types
        if instance_type_ids_to_delete:
            instance_type_api_client.delete_many(list(instance_type_ids_to_delete))
        self.api_endpoint_client.update(
            self.registration_id,
            {
                self.instance_types_property_name: updated_instance_type_ids
                + new_instance_type_ids,
            },
        )

    def add_instance_type_formset(
        self,
        form_class,
        formset_prefix: str,
        base_formset_class,
        api_endpoint_client_class,
        formset_processing_function,
        can_delete: bool | None = None,
        extra_formset_factory_kwargs: dict | None = None,
    ):
        self.manually_processed_formsets[formset_prefix] = {
            "api_endpoint_client_class": api_endpoint_client_class,
            "formset_processing_function": formset_processing_function,
        }
        return self.add_formset_class(
            form_class,
            formset_prefix,
            base_formset_class=base_formset_class,
            can_delete=can_delete,
            extra_formset_factory_kwargs=extra_formset_factory_kwargs,
            add_to_main_form=False,
        )

    def get_instance_type_formset_initial(self):
        initial = list()
        instance_type_ids = self.registration.get(self.instance_types_property_name)
        if not all(
            isinstance(instance_type_id, int) for instance_type_id in instance_type_ids
        ):
            return initial
        instance_type_api_client = InstanceTypeApiEndpointClient()
        instance_types = instance_type_api_client.get_registrations_by_ids(
            instance_type_ids
        )
        if not instance_types or not isinstance(instance_types, list):
            instance_types = list()
        for instance_type in instance_types:
            initial.append(instance_type)
        return initial

    # EditorProcessFormView
    def setup(self, request, *args, **kwargs):
        self.manually_processed_formsets = dict()
        return super().setup(request, *args, **kwargs)

    def forms_valid(self, forms: dict):
        response = super().forms_valid(forms)
        for (
            formset_prefix,
            formset_metadata,
        ) in self.manually_processed_formsets.items():
            api_endpoint_client_class = formset_metadata.get(
                "api_endpoint_client_class"
            )
            formset_processing_function = formset_metadata.get(
                "formset_processing_function"
            )
            if not formset_processing_function:
                continue
            formset_processing_function(
                forms.get(formset_prefix), api_endpoint_client_class
            )
        return response

    # ProcessFormView
    def dispatch(self, request, *args, **kwargs):
        self.instance_types_property_name = "instance_types"
        self.add_instance_type_formset(
            InstanceTypeEditorForm,
            self.instance_types_property_name,
            InstanceTypeFormSet,
            InstanceTypeApiEndpointClient,
            self.process_instance_types,
            extra_formset_factory_kwargs={
                "extra": 0,
            },
        )

        # Configure initial formset data
        initial = self.get_instance_type_formset_initial()
        self.add_initial_data_for_formset(initial, self.instance_types_property_name)
        self.exclude_formset_from_table_templates(self.instance_types_property_name)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "instance_type_list_item_template": render_to_string(
                    "instance_types/instance_type_list_item.html",
                    {
                        "form": (
                            context.get("formsets", {})
                            .get(self.instance_types_property_name)
                            .empty_form
                        ),
                    },
                ),
            }
        )
        return context


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = "capacities:cloud_capacities_list"
    editor_url_reverse_base = "capacities:cloud_capacity_editor"
    editor_start_url_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_url_reverse_base = "capacities:cloud_capacity_overview"
    registration_type_name_singular = "cloud capacity"
    registration_type_name_plural = "cloud capacities"
    api_endpoint_client_class = CloudCapacityApiEndpointClient
    column_metadata_api_endpoint_client_class = (
        CloudCapacityColumnMetadataApiEndpointClient
    )


class CloudCapacityEditorStartFormView(
    CloudCapacityEditorView, EditorStartFormView, FormView
):
    template_name = "capacities/new_cloud_capacity_start.html"
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorProcessFormView(
    CloudCapacityEditorView, EditorProcessFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    main_form_class = CloudCapacityEditorForm
    success_url = reverse_lazy("capacities:new_cloud_capacity")


class CloudCapacityMetadataEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityMetadataEditorProcessFormView
):
    pass


class CloudCapacityCostAndLocalityEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityCostAndLocalityEditorProcessFormView
):
    pass


class CloudCapacityEnergyEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityEnergyEditorProcessFormView
):
    pass


class CloudCapacitySecurityTrustAndAccessEditorProcessFormView(
    CloudCapacityEditorProcessFormView,
    CapacitySecurityTrustAndAccessEditorProcessFormView,
):
    pass


class CloudCapacitySystemSpecificEditorProcessFormView(
    CloudCapacityEditorProcessFormView,
    MultipleEditorFormsetProcessFormView,
    ArchitectureFormSetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
):
    def dispatch(self, request, *args, **kwargs):
        self.add_architecture_formset_metadata()
        self.add_operating_system_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class CloudCapacitySpecsEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacitySpecsEditorProcessFormView
):
    pass


class CloudCapacityEditorRouterView(CloudCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = CloudCapacityEditorProcessFormView
    metadata_editor_view_class = CloudCapacityMetadataEditorProcessFormView
    cost_and_locality_editor_view_class = (
        CloudCapacityCostAndLocalityEditorProcessFormView
    )
    energy_editor_view_class = CloudCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = (
        CloudCapacitySecurityTrustAndAccessEditorProcessFormView
    )
    specs_editor_view_class = CloudCapacitySpecsEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "system specific":
            return CloudCapacitySystemSpecificEditorProcessFormView.as_view()(
                request, *args, **kwargs
            )
        return super().route_to_view(request, *args, **kwargs)


class CloudCapacityRegistrationsListFormView(
    CloudCapacityEditorView, RegistrationsListFormView
):
    template_name = "capacities/cloud_capacities.html"
    new_registration_reverse = "capacities:new_cloud_capacity"


class CloudCapacityEditorOverviewTemplateView(
    CloudCapacityEditorView, EditorOverviewTemplateView
):
    template_name = "capacities/cloud_capacity_overview.html"


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = "capacities:edge_capacities_list"
    editor_url_reverse_base = "capacities:edge_capacity_editor"
    editor_start_url_reverse_base = "capacities:new_edge_capacity"
    editor_overview_url_reverse_base = "capacities:edge_capacity_overview"
    registration_type_name_singular = "edge capacity"
    registration_type_name_plural = "edge capacities"
    title_base = "New Edge Capacity"
    api_endpoint_client_class = EdgeCapacityApiEndpointClient
    column_metadata_api_endpoint_client_class = (
        EdgeCapacityColumnMetadataApiEndpointClient
    )


class EdgeCapacityEditorStartFormView(EdgeCapacityEditorView, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorProcessFormView(EdgeCapacityEditorView, EditorProcessFormView):
    template_name = "capacities/edge_capacity_editor.html"
    main_form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy("capacities:new_edge_capacity")


class EdgeCapacityMetadataEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityMetadataEditorProcessFormView
):
    pass


class EdgeCapacityCostAndLocalityEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityCostAndLocalityEditorProcessFormView
):
    pass


class EdgeCapacityEnergyEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityEnergyEditorProcessFormView
):
    pass


class EdgeCapacitySpecificEditorProcessFormView(
    EdgeCapacityEditorProcessFormView,
    MultipleEditorFormsetProcessFormView,
    AccessibleSensorsFormsetEditorViewMixin,
    DevicesFormsetEditorViewMixin,
):
    def dispatch(self, request, *args, **kwargs):
        self.add_accessible_sensors_formset_metadata()
        self.add_devices_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacitySecurityTrustAndAccessEditorProcessFormView(
    EdgeCapacityEditorProcessFormView,
    CapacitySecurityTrustAndAccessEditorProcessFormView,
):
    pass


class EdgeCapacitySpecsEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacitySpecsEditorProcessFormView
):
    pass


class EdgeCapacityEditorRouterView(EdgeCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = EdgeCapacityEditorProcessFormView
    metadata_editor_view_class = EdgeCapacityMetadataEditorProcessFormView
    cost_and_locality_editor_view_class = (
        EdgeCapacityCostAndLocalityEditorProcessFormView
    )
    energy_editor_view_class = EdgeCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = (
        EdgeCapacitySecurityTrustAndAccessEditorProcessFormView
    )
    specs_editor_view_class = EdgeCapacitySpecsEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "edge specific":
            return EdgeCapacitySpecificEditorProcessFormView.as_view()(
                request, *args, **kwargs
            )
        return super().route_to_view(request, *args, **kwargs)


class EdgeCapacityRegistrationsListFormView(
    EdgeCapacityEditorView, RegistrationsListFormView
):
    template_name = "capacities/edge_capacities.html"
    new_registration_reverse = "capacities:new_edge_capacity"


class EdgeCapacityEditorOverviewTemplateView(
    EdgeCapacityEditorView, EditorOverviewTemplateView
):
    template_name = "capacities/edge_capacity_overview.html"

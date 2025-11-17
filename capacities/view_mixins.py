from django.urls import reverse_lazy

from .forms import (
    CapacityGetLocalityByGpsForm,
    CapacityLocalityEditorForm,
    CapacityLocalityOptionsSearchForm,
    CloudCapacityArchitectureEditorForm,
    CloudCapacityOperatingSystemEditorForm,
    EdgeCapacityAccessibleSensorsEditorForm,
    EdgeCapacityDevicesEditorForm,
)
from .formsets import (
    CloudCapacityArchitectureEditorFormSet,
    CapacityLocalityEditorFormSet,
    CloudCapacityOperatingSystemEditorFormSet,
    EdgeCapacityAccessibleSensorsEditorFormSet,
    EdgeCapacityDevicesEditorFormSet,
)


# Cloud capacities
class ArchitectureFormSetEditorViewMixin:
    def add_architecture_formset_metadata(self):
        property_name = 'architecture'
        self.add_formset_class(
            CloudCapacityArchitectureEditorForm,
            property_name,
            base_formset_class=CloudCapacityArchitectureEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        architecture_names = self.registration.get(property_name)
        if not architecture_names:
            architecture_names = list()
        for architecture_name in architecture_names:
            initial.append({
                'architecture_name': architecture_name,
            })
        self.add_initial_data_for_formset(initial, property_name)


class LocalityFormSetEditorViewMixin:
    def add_locality_formset_metadata(self):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'locality_options_search_form': CapacityLocalityOptionsSearchForm(prefix='locality'),
            'locality_options_search_form_url_reverse': reverse_lazy('capacities:locality_options_search'),
            'get_locality_by_gps_form': CapacityGetLocalityByGpsForm(prefix='locality'),
            'get_locality_by_name_url_reverse': reverse_lazy('capacities:get_locality_by_name'),
            'get_locality_by_gps_url_reverse': reverse_lazy('capacities:get_locality_by_gps'),
        })
        return context


class OperatingSystemFormSetEditorViewMixin:
    def add_operating_system_formset_metadata(self):
        property_name = 'operating_system'
        self.add_formset_class(
            CloudCapacityOperatingSystemEditorForm,
            property_name,
            base_formset_class=CloudCapacityOperatingSystemEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        operating_systems = self.registration.get(property_name)
        if (not operating_systems
            or not isinstance(operating_systems, dict)):
            operating_systems = dict()
        for os_name, os_id in operating_systems.items():
            initial.append({
                'os_name': os_name,
                'os_id': os_id,
            })
        self.add_initial_data_for_formset(initial, property_name)


# Edge capacities
class AccessibleSensorsFormsetEditorViewMixin:
    def add_accessible_sensors_formset_metadata(self):
        property_name = 'accessible_sensors'
        self.add_formset_class(
            EdgeCapacityAccessibleSensorsEditorForm,
            property_name,
            base_formset_class=EdgeCapacityAccessibleSensorsEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        sensor_names = self.registration.get(property_name)
        if not sensor_names:
            sensor_names = list()
        for sensor_name in sensor_names:
            initial.append({
                'sensor_name': sensor_name,
            })
        self.add_initial_data_for_formset(initial, property_name)


class DevicesFormsetEditorViewMixin:
    def add_devices_formset_metadata(self):
        property_name = 'devices'
        self.add_formset_class(
            EdgeCapacityDevicesEditorForm,
            property_name,
            base_formset_class=EdgeCapacityDevicesEditorFormSet
        )

        # Configure initial formset data
        initial = list()
        devices = self.registration.get(property_name)
        if not devices:
            devices = dict()
        for device_type, device_name in devices.items():
            initial.append({
                'device_type': device_type,
                'device_name': device_name,
            })
        self.add_initial_data_for_formset(initial, property_name)

from .forms import (
    CloudCapacityArchitectureEditorForm,
    CloudCapacityOperatingSystemEditorForm,
    EdgeCapacityAccessibleSensorsEditorForm,
    EdgeCapacityDevicesEditorForm,
)
from .formsets import (
    CloudCapacityArchitectureEditorFormSet,
    CloudCapacityOperatingSystemEditorFormSet,
    EdgeCapacityAccessibleSensorsEditorFormSet,
    EdgeCapacityDevicesEditorFormSet,
)


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

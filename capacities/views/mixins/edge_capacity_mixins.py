# Forms
from capacities.forms.edge_capacity_forms import (
    EdgeCapacityAccessibleSensorsEditorForm,
    EdgeCapacityDevicesEditorForm,
)

# Formsets
from capacities.formsets.edge_capacity_formsets import (
    EdgeCapacityAccessibleSensorsEditorFormSet,
    EdgeCapacityDevicesEditorFormSet,
)


# Edge capacities
class AccessibleSensorsFormsetEditorViewMixin:
    def add_accessible_sensors_formset_metadata(self):
        property_name = "accessible_sensors"
        self.add_formset_class(
            EdgeCapacityAccessibleSensorsEditorForm,
            property_name,
            base_formset_class=EdgeCapacityAccessibleSensorsEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        sensor_names = self.registration.get(property_name)
        if not sensor_names:
            sensor_names = list()
        for sensor_name in sensor_names:
            initial.append(
                {
                    "sensor_name": sensor_name,
                }
            )
        self.add_initial_data_for_formset(initial, property_name)


class DevicesFormsetEditorViewMixin:
    def add_devices_formset_metadata(self):
        property_name = "devices"
        self.add_formset_class(
            EdgeCapacityDevicesEditorForm,
            property_name,
            base_formset_class=EdgeCapacityDevicesEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        devices = self.registration.get(property_name)
        if not devices:
            devices = dict()
        for device_type, device_name in devices.items():
            initial.append(
                {
                    "device_type": device_type,
                    "device_name": device_name,
                }
            )
        self.add_initial_data_for_formset(initial, property_name)

# Forms
from capacities.forms.cloud_capacity_forms import (
    CloudCapacityArchitectureEditorForm,
    CloudCapacityOperatingSystemEditorForm,
)

# Formsets
from capacities.formsets.cloud_capacity_formsets import (
    CloudCapacityArchitectureEditorFormSet,
    CloudCapacityOperatingSystemEditorFormSet,
)


# Cloud capacities
class ArchitectureFormSetEditorViewMixin:
    def add_architecture_formset_metadata(self):
        property_name = "architecture"
        self.add_formset_class(
            CloudCapacityArchitectureEditorForm,
            property_name,
            base_formset_class=CloudCapacityArchitectureEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        architecture_names = self.resource.get(property_name)
        if not architecture_names:
            architecture_names = list()
        for architecture_name in architecture_names:
            initial.append(
                {
                    "architecture_name": architecture_name,
                }
            )
        self.add_initial_data_for_formset(initial, property_name)


class OperatingSystemFormSetEditorViewMixin:
    def add_operating_system_formset_metadata(self):
        property_name = "operating_system"
        self.add_formset_class(
            CloudCapacityOperatingSystemEditorForm,
            property_name,
            base_formset_class=CloudCapacityOperatingSystemEditorFormSet,
        )

        # Configure initial formset data
        initial = list()
        operating_systems = self.resource.get(property_name)
        if not operating_systems or not isinstance(operating_systems, dict):
            operating_systems = dict()
        for os_name, os_id in operating_systems.items():
            initial.append(
                {
                    "os_name": os_name,
                    "os_id": os_id,
                }
            )
        self.add_initial_data_for_formset(initial, property_name)

from django.template.loader import render_to_string

from capacities.forms.capacity_forms import (
    CapacityEnergyConsumptionEditorForm,
    CapacityPriceEditorForm,
    CapacitySecurityPortsEditorForm,
)
from capacities.formsets.capacity_formsets import (
    CapacityEnergyConsumptionEditorFormSet,
    CapacityPriceEditorFormSet,
    CapacitySecurityPortsEditorFormSet,
)

# from capacity_instance_types.api.api_clients import CapacityInstanceTypeApiClient
from capacity_instance_types.api.mocks.mock_api_clients import (
    CapacityInstanceTypeApiClient,
)
from capacity_instance_types.forms import CapacityInstanceTypeEditorForm
from capacity_instance_types.formsets import CapacityInstanceTypeFormSet
from editor.views import (
    EditorRouterView,
    MultipleEditorFormsetProcessFormView,
)
from localities.views import LocalityFormSetEditorViewMixin


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
        price_data = self.resource.get(price_property_name)
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
        energy_consumption_data = self.resource.get(property_name)
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
        security_ports = self.resource.get(property_name)
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
        formset: CapacityInstanceTypeFormSet,
        api_client_class: CapacityInstanceTypeApiClient,
    ):
        instance_type_api_client = api_client_class()
        inst_type_id_field_name = instance_type_api_client.endpoint_definition.id_field
        current_instance_type_id_strs = list(
            map(str, self.resource.get("instance_types"))
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
        self.api_client.update(
            self.resource_id,
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
        api_client_class,
        formset_processing_function,
        can_delete: bool | None = None,
        extra_formset_factory_kwargs: dict | None = None,
    ):
        self.manually_processed_formsets[formset_prefix] = {
            "api_client_class": api_client_class,
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
        instance_type_ids = self.resource.get(self.instance_types_property_name, list())
        if not isinstance(instance_type_ids, list):
            instance_type_ids = list()
        if not all(
            isinstance(instance_type_id, int) for instance_type_id in instance_type_ids
        ):
            return initial
        instance_type_api_client = CapacityInstanceTypeApiClient()
        instance_types = instance_type_api_client.get_resources_by_ids(
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
            api_client_class = formset_metadata.get("api_client_class")
            formset_processing_function = formset_metadata.get(
                "formset_processing_function"
            )
            if not formset_processing_function:
                continue
            formset_processing_function(forms.get(formset_prefix), api_client_class)
        return response

    # ProcessFormView
    def dispatch(self, request, *args, **kwargs):
        self.instance_types_property_name = "instance_types"
        self.add_instance_type_formset(
            CapacityInstanceTypeEditorForm,
            self.instance_types_property_name,
            CapacityInstanceTypeFormSet,
            CapacityInstanceTypeApiClient,
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
                    "capacity_instance_types/capacity_instance_type_list_item.html",
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

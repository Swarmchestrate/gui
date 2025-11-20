from django.urls import reverse_lazy

from capacities.forms.capacity_forms import (
    CapacityGetLocalityByGpsForm,
    CapacityLocalityEditorForm,
    CapacityLocalityOptionsSearchForm,
)
from capacities.formsets.capacity_formsets import CapacityLocalityEditorFormSet


class LocalityFormSetEditorViewMixin:
    def add_locality_formset_metadata(self):
        locality_property_name = "locality_id"
        self.add_formset_class(
            CapacityLocalityEditorForm,
            locality_property_name,
            base_formset_class=CapacityLocalityEditorFormSet,
            can_delete=False,
            extra_formset_factory_kwargs={
                "extra": 0,
                "max_num": 1,
            },
        )

        # Configure initial formset data
        initial_locality = list()
        locality_data = self.registration.get(locality_property_name)
        if not locality_data or not isinstance(locality_data, dict):
            locality_data = {
                "continent": "",
                "country": "",
                "city": "",
                "gps": "",
            }
        initial_locality.append(locality_data)
        self.add_initial_data_for_formset(initial_locality, locality_property_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "locality_options_search_form": CapacityLocalityOptionsSearchForm(
                    prefix="locality"
                ),
                "locality_options_search_form_url_reverse": reverse_lazy(
                    "capacities:locality_options_search"
                ),
                "get_locality_by_gps_form": CapacityGetLocalityByGpsForm(
                    prefix="locality"
                ),
                "get_locality_by_name_url_reverse": reverse_lazy(
                    "capacities:get_locality_by_name"
                ),
                "get_locality_by_gps_url_reverse": reverse_lazy(
                    "capacities:get_locality_by_gps"
                ),
            }
        )
        return context

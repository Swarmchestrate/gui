from django.urls import reverse_lazy

from editor.forms.helpers.locality_forms import (
    GetLocalityByGpsForm,
    LocalityEditorForm,
    LocalityOptionsSearchForm,
)
from editor.formsets.helpers.locality_formsets import LocalityEditorFormSet


class LocalityFormSetEditorViewMixin:
    def add_locality_formset_metadata(self):
        self.locality_property_name = "locality_id"
        self.add_formset_class(
            LocalityEditorForm,
            self.locality_property_name,
            base_formset_class=LocalityEditorFormSet,
            can_delete=False,
            extra_formset_factory_kwargs={
                "extra": 0,
                "max_num": 1,
            },
        )

        # Configure initial formset data
        initial_locality = list()
        locality_data = self.registration.get(self.locality_property_name)
        if not locality_data or not isinstance(locality_data, dict):
            locality_data = {
                "form_prefix": self.locality_property_name,
                "continent": "",
                "country": "",
                "city": "",
                "gps": "",
            }
        initial_locality.append(locality_data)
        self.add_initial_data_for_formset(initial_locality, self.locality_property_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "locality_options_search_form": LocalityOptionsSearchForm(
                    prefix=self.locality_property_name
                ),
                "get_locality_by_gps_form": GetLocalityByGpsForm(
                    prefix=self.locality_property_name
                ),
                "locality_options_search_form_url_reverse": reverse_lazy(
                    "editor:locality_options_search"
                ),
                "get_locality_by_name_url_reverse": reverse_lazy(
                    "editor:get_locality_by_name"
                ),
                "get_locality_by_gps_url_reverse": reverse_lazy(
                    "editor:get_locality_by_gps"
                ),
            }
        )
        return context

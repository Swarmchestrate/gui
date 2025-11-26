from http import HTTPStatus

import geonamescache
import reverse_geocode
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import ProcessFormView

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    ResourceTypeNameContextMixin,
)
from resource_management.views import ResourceListContextMixin

from .api.api_clients import LocalityApiClient, LocalityColumnMetadataApiClient
from .forms import (
    GetLocalityByGpsForm,
    GetLocalityByNameForm,
    LocalityEditorForm,
    LocalityOptionsSearchForm,
)
from .formsets import LocalityEditorFormSet


class LocalityViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = LocalityApiClient
    column_metadata_api_client_class = LocalityColumnMetadataApiClient
    editor_resource_list_url_reverse = "localities:localities_list"
    resource_type_name_singular = "locality"
    resource_type_name_plural = "localities"


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
        locality_data = self.resource.get(self.locality_property_name)
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
                    "localities:locality_options_search"
                ),
                "get_locality_by_name_url_reverse": reverse_lazy(
                    "localities:get_locality_by_name"
                ),
                "get_locality_by_gps_url_reverse": reverse_lazy(
                    "localities:get_locality_by_gps"
                ),
            }
        )
        return context


class CapacityLocalityOptionsSearchProcessFormView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        form = LocalityOptionsSearchForm(data=request.GET)
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
        form = GetLocalityByNameForm(data=request.GET)
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
        form = GetLocalityByGpsForm(data=request.GET)
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

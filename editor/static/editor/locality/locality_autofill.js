import { localityFormPrefix } from "/static/editor/locality/locality_section.js";

export function getEmptyLocalityTemplate() {
    return {
        continent: "",
        country: "",
        city: "",
        latitude: "",
        longitude: "",
    };
}

export function fillLocalityAutomatically(locality) {
    const manualLocationEntry = document.querySelector(
        "#manual-location-entry",
    );
    manualLocationEntry.open = true;
    // Continent
    const localityContinentInput = document.querySelector(
        `#id_${localityFormPrefix}-0-continent`,
    );
    localityContinentInput.value = locality.continent;
    // Country
    const localityCountryInput = document.querySelector(
        `#id_${localityFormPrefix}-0-country`,
    );
    localityCountryInput.value = locality.country;
    // City
    const localityCityInput = document.querySelector(
        `#id_${localityFormPrefix}-0-city`,
    );
    localityCityInput.value = locality.city;
    // GPS Co-ordinates
    const localityGpsLocationInput = document.querySelector(
        `#id_${localityFormPrefix}-0-gps`,
    );
    const coordinates = [];
    if (locality.latitude) {
        coordinates.push(locality.latitude);
    }
    if (locality.longitude) {
        coordinates.push(locality.longitude);
    }
    localityGpsLocationInput.value = `${coordinates.join(", ")}`;
}

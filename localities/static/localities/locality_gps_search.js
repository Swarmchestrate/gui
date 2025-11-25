import {
    getEmptyLocalityTemplate,
    fillLocalityAutomatically,
} from "/static/localities/locality_autofill.js";
import { localityFormPrefix } from "/static/localities/locality_section.js";

const latitudeInputSelector = `input[name='${localityFormPrefix}-gps_location_latitude']`;
const longitudeInputSelector = `input[name='${localityFormPrefix}-gps_location_longitude']`;

async function getLocalityByGpsLocation(latitude, longitude) {
    const locality = getEmptyLocalityTemplate();
    const getLocalityByGpsUrl = document.querySelector(
        "#get-locality-by-gps-url",
    ).value;
    const response = await fetch(
        `${getLocalityByGpsUrl}?${new URLSearchParams({
            gps_location_latitude: latitude,
            gps_location_longitude: longitude,
        }).toString()}`,
        {
            method: "GET",
        },
    );
    if (!response.ok) {
        return locality;
    }
    const responseContent = await response.json();
    locality.continent = responseContent.continent;
    locality.country = responseContent.country;
    locality.city = responseContent.city;
    locality.latitude = latitude;
    locality.longitude = longitude;
    return locality;
}

function setupGpsLocationSearch() {
    const findByGpsButton = document.querySelector("#find-by-gps-button");
    if (!findByGpsButton) {
        return;
    }
    const latitudeInput = document.querySelector(latitudeInputSelector);
    const longitudeInput = document.querySelector(longitudeInputSelector);
    findByGpsButton.addEventListener("click", async () => {
        findByGpsButton
            .querySelector(".spinner-wrapper")
            .classList.remove("d-none");
        const locality = await getLocalityByGpsLocation(
            latitudeInput.value,
            longitudeInput.value,
        );
        findByGpsButton
            .querySelector(".spinner-wrapper")
            .classList.add("d-none");
        fillLocalityAutomatically(locality);
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setupGpsLocationSearch();
});

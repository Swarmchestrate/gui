const latitudeInputSelector = "input[name='locality-gps_location_latitude']";
const longitudeInputSelector = "input[name='locality-gps_location_longitude']";

async function getLocalityByGpsLocation(latitude, longitude) {
    const emptyLocality = {
        continent: "",
        country: "",
        city: "",
    };
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
        return emptyLocality;
    }
    const locality = await response.json();
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
        const localityContinentInput = document.querySelector(
            "#id_locality-0-continent",
        );
        localityContinentInput.value = locality.continent;
        const localityCountryInput = document.querySelector(
            "#id_locality-0-country",
        );
        localityCountryInput.value = locality.country;
        const localityCityInput = document.querySelector("#id_locality-0-city");
        localityCityInput.value = locality.city;
        const localityGpsLocationInput =
            document.querySelector("#id_locality-0-gps");
        localityGpsLocationInput.value = `${latitudeInput.value}, ${longitudeInput.value}`;
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setupGpsLocationSearch();
});

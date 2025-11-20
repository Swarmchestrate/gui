import {
    getEmptyLocalityTemplate,
    fillLocalityAutomatically,
} from "/static/editor/locality/locality_autofill.js";
import { localityFormPrefix } from "/static/editor/locality/locality_section.js";

async function getLocalityOptions(query, localityOptionsSearchUrl) {
    const response = await fetch(
        `${localityOptionsSearchUrl}?${new URLSearchParams({
            query: query,
        }).toString()}`,
        {
            method: "GET",
        },
    );
    if (!response.ok) {
        return [];
    }
    const content = await response.json();
    return content.options;
}

async function getLocality(value, getLocalityUrl) {
    const locality = getEmptyLocalityTemplate();
    const [localityType, geonameId, label] = value.split("_");
    let continentCode = "",
        countryCode = "",
        cityName = "";
    switch (localityType) {
        case "continent":
            continentCode = label;
            break;
        case "country":
            countryCode = label;
            break;
        case "city":
            cityName = label;
            break;
    }
    const response = await fetch(
        `${getLocalityUrl}?${new URLSearchParams({
            geoname_id: geonameId,
            continent_code: continentCode,
            country_code: countryCode,
            city_name: cityName,
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
    return locality;
}

function setupLocalityTomSelect(localityOptionsSearchUrl) {
    const localityTomSelect = new TomSelect(`#id_${localityFormPrefix}-query`, {
        valueField: "value",
        labelField: "name",
        searchField: "name",
        optgroupField: "optgroup",
        optgroupValueField: "value",
        optgroupLabelField: "label",
        optgroups: [
            { value: "continents", label: "Continents" },
            { value: "countries", label: "Countries" },
            { value: "cities", label: "Cities" },
        ],
        load: async (query, callback) => {
            const options = await getLocalityOptions(
                query,
                localityOptionsSearchUrl,
            );
            if (!options.length) {
                return callback();
            }
            return callback(options);
        },
        render: {
            option: (data, escape) => {
                let optionContent = escape(data.name);
                if ("country_name" in data) {
                    optionContent += `
                    <small class="text-body-tertiary ms-1">
                        ${escape(data.country_name)}
                    </small>`;
                }
                return `<div>
                    ${optionContent}
                </div>`;
            },
            loading: (data, escape) => {
                return `<div
                    class="spinner-border text-body-tertiary mx-3"
                    style="width: 1.5rem; height: 1.5rem;">
                </div>`;
            },
        },
    });
    localityTomSelect.on("change", async (value) => {
        const getLocalityUrlInput = document.querySelector(
            "#get-locality-by-name-url",
        );
        if (!getLocalityUrlInput) {
            return;
        }
        const getLocalityUrl = getLocalityUrlInput.value;
        const locality = await getLocality(value, getLocalityUrl);
        fillLocalityAutomatically(locality);
    });
    return localityTomSelect;
}

function setupLocalitySearch() {
    const localityOptionsSearchUrlInput = document.querySelector(
        "#locality-options-search-url",
    );
    if (!localityOptionsSearchUrlInput) {
        return;
    }
    const localityOptionsSearchUrl = localityOptionsSearchUrlInput.value;
    const localityTomSelect = setupLocalityTomSelect(localityOptionsSearchUrl);
}

window.addEventListener("DOMContentLoaded", () => {
    setupLocalitySearch();
});

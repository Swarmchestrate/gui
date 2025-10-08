function setupLocalitySearch() {
    const localitySearchUrlInput = document.querySelector(
        "#locality-search-url",
    );
    if (!localitySearchUrlInput) {
        return;
    }
    const localitySearchUrl = localitySearchUrlInput.value;
    const tomSelect = new TomSelect("#id_locality-query", {
        valueField: "name",
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
        load: async function (query, callback) {
            const response = await fetch(
                `${localitySearchUrl}?${new URLSearchParams({
                    query: query,
                }).toString()}`,
                {
                    method: "GET",
                },
            );
            if (!response.ok) {
                return callback();
            }
            const content = await response.json();
            const options = content.options;
            return callback(options);
        },
        render: {
            loading: function (data, escape) {
                return `<div
                            class="spinner-border text-body-tertiary mx-3"
                            style="width: 1.5rem; height: 1.5rem;"></div>`;
            },
        },
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setupLocalitySearch();
});

function toggleDeleteUi(button, table) {
    if (!table.classList.contains("delete-disabled")) {
        button.removeAttribute("aria-pressed");
        button.classList.remove("active");
        return table.classList.add("delete-disabled");
    }
    button.setAttribute("aria-pressed", "true");
    button.classList.add("active");
    return table.classList.remove("delete-disabled");
}

function addRow(tableBody, templateRow) {
    const nextIndex = tableBody.querySelectorAll("tr").length;
    const newRow = templateRow.cloneNode(true);
    const templateElements = newRow.querySelectorAll(
        '[id*="__prefix__"], [for*="__prefix__"], [name*="__prefix__"]',
    );
    for (const element of templateElements) {
        for (const attribute of element.attributes) {
            if (!attribute.value.includes("__prefix__")) {
                continue;
            }
            element.setAttribute(
                attribute.name,
                attribute.value.replace("__prefix__", nextIndex),
            );
        }
    }
    tableBody.appendChild(newRow);
}

export function setupFormsetTables() {
    const formsetTables = document.querySelectorAll(".formset-table");
    for (const formsetTable of formsetTables) {
        const formsetPrefix = formsetTable.dataset.formsetPrefix;
        const tableBody = formsetTable.querySelector("tbody");
        const templateRow = document.querySelector(
            `table.formset-template-table[data-formset-prefix="${formsetPrefix}"] tr`,
        );
        const addRowButton = document.querySelector(
            `button.formset-table-add-row-button[data-table-id="${formsetTable.id}"]`,
        );
        addRowButton.addEventListener("click", () => {
            addRow(tableBody, templateRow);
        });
        const deleteRowsButton = document.querySelector(
            `button.formset-table-delete-rows-button[data-table-id="${formsetTable.id}"]`,
        );
        deleteRowsButton.addEventListener("click", () => {
            toggleDeleteUi(deleteRowsButton, formsetTable);
        });
    }
}

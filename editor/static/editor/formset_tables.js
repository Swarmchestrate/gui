// Deleting rows
function toggleDeleteUi(checkbox, table) {
    if (checkbox.checked) {
        return table.classList.remove("delete-disabled");
    }
    return table.classList.add("delete-disabled");
}

function setupDeleteCheckbox(deleteCheckbox, tableRow) {
    deleteCheckbox.addEventListener("input", () => {
        if (deleteCheckbox.checked) {
            return tableRow.classList.add("table-danger");
        }
        return tableRow.classList.remove("table-danger");
    });
}

// Adding rows
function addRow(tableBody, templateRow, totalFormsetInput) {
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
    totalFormsetInput.value = parseInt(totalFormsetInput.value) + 1;
}

export function setupFormsetTables() {
    const formsetTables = document.querySelectorAll(".formset-table");
    for (const formsetTable of formsetTables) {
        const formsetPrefix = formsetTable.dataset.formsetPrefix;
        const formsetTotalInput = document.querySelector(
            `input[name="${formsetPrefix}-TOTAL_FORMS"]`,
        );
        const tableBody = formsetTable.querySelector("tbody");
        const tableRows = tableBody.querySelectorAll("tr");
        for (const tableRow of tableRows) {
            const deleteCheckbox = tableRow.querySelector(
                `input[type="checkbox"][name$="-DELETE"]`,
            );
            if (!deleteCheckbox) continue;
            setupDeleteCheckbox(deleteCheckbox, tableRow);
        }
        const templateRow = document.querySelector(
            `table.formset-template-table[data-formset-prefix="${formsetPrefix}"] tr`,
        );
        const addRowButton = document.querySelector(
            `button.formset-table-add-row-button[data-table-id="${formsetTable.id}"]`,
        );
        addRowButton.addEventListener("click", () => {
            addRow(tableBody, templateRow, formsetTotalInput);
        });
        const deleteRowsCheckbox = document.querySelector(
            `input.formset-should-delete-rows[type="checkbox"][data-table-id="${formsetTable.id}"]`,
        );
        deleteRowsCheckbox.addEventListener("input", () => {
            toggleDeleteUi(deleteRowsCheckbox, formsetTable);
        });
    }
}

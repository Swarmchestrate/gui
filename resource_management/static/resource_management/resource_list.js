import { setupDialog } from "/static/dialog.js";

const form = document.getElementById("resource-deletion-form");
const resourcesTableBody = document.querySelector("#resources-table tbody");
const deleteCheckedButton = document.getElementById("delete-checked-btn");
const numCheckedElement = document.getElementById("num-checked");

const deleteDialog = document.querySelector("#delete-dialog");
const deleteMultipleDialog = document.querySelector("#delete-multiple-dialog");

// DataTables setup
function initialiseDataTable() {
    DataTable.datetime("dd/MM/yyyy, HH:mm:ss");
    const dataTable = new DataTable("#resources-table", {
        columnDefs: [
            {
                orderable: false,
                render: DataTable.render.select(),
                target: 0,
            },
        ],
        columns: [
            { name: "checkbox" },
            { name: "id" },
            { name: "date_created" },
            { name: "date_updated" },
            { name: "actions" },
        ],
        select: {
            style: "os",
            selector: "td:first-child",
        },
        order: {
            name: "date_updated",
            dir: "desc",
        },
    });
    return dataTable;
}

function getAllSelectedRows() {
    return resourcesTableBody.querySelectorAll(
        "input[type='checkbox']:checked",
    );
}

function updateDeleteCheckedButtonState(numChecked) {
    numCheckedElement.textContent = numChecked;
    if (numChecked === 0) {
        return deleteCheckedButton.classList.add("invisible");
    }
    return deleteCheckedButton.classList.remove("invisible");
}

function setupDataTableEventListeners(dataTable) {
    dataTable.on("select", (e, dt, type, indexes) => {
        if (type !== "row") {
            return;
        }
        const selected = dataTable.rows(indexes).nodes().toArray();
        selected.forEach((row) => {
            row.classList.add("table-active");
        });
    });

    dataTable.on("deselect", (e, dt, type, indexes) => {
        if (type !== "row") {
            return;
        }
        const deselected = dataTable.rows(indexes).nodes().toArray();
        deselected.forEach((row) => {
            row.classList.remove("table-active");
        });
    });
}

function initialiseAndSetupDataTable() {
    const dataTable = initialiseDataTable();
    setupDataTableEventListeners(dataTable);
    return dataTable;
}

// Table row setup
function setupRegistrationsTableCheckboxStyling(checkbox) {
    return checkbox.classList.add("form-check-input");
}

function setupRegistrationsTableInputsAndButtons() {
    const selectAllRowsCheckbox = document.querySelector(
        "#resources-table thead input[type='checkbox']",
    );
    setupRegistrationsTableCheckboxStyling(selectAllRowsCheckbox);
    selectAllRowsCheckbox.addEventListener("input", () => {
        // Small timeout added before updating delete checked
        // button state as number of selected rows doesn't
        // update straight away.
        window.setTimeout(() => {
            updateDeleteCheckedButtonState(getAllSelectedRows().length);
        }, 25);
    });
    const tableRows = resourcesTableBody.querySelectorAll("tr");
    tableRows.forEach((tr) => {
        // Select row checkbox
        const checkbox = tr.querySelector("input[type='checkbox']");
        setupRegistrationsTableCheckboxStyling(checkbox);
        checkbox.addEventListener("input", () => {
            updateDeleteCheckedButtonState(getAllSelectedRows().length);
        });
        checkbox.setAttribute("name", "resource_ids_to_delete");
        const resourceId = tr.dataset.resourceId;
        if (!resourceId) {
            return;
        }
        checkbox.setAttribute("value", resourceId);
        // Delete row button
        const deleteButton = tr.querySelector(".delete-btn");
        deleteButton.addEventListener("click", () => {
            deleteDialog
                .querySelector(".confirm-btn")
                .setAttribute("value", tr.dataset.resourceId);

            deleteDialog.querySelector(".dialog-id-to-delete").textContent =
                tr.dataset.resourceId;
        });
    });
    // Delete dialog setup
    const deleteButtons = resourcesTableBody.querySelectorAll(".delete-btn");
    setupDialog(
        deleteDialog,
        [deleteDialog.querySelector(".btn-close")],
        deleteButtons,
    );
    deleteDialog.addEventListener("close", (e) => {
        const returnValue = deleteDialog.returnValue;
        if (returnValue === "cancel" || returnValue === "") {
            return;
        }
        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = "resource_ids_to_delete";
        hiddenInput.value = returnValue;
        form.appendChild(hiddenInput);
        form.submit();
    });
}

window.addEventListener("DOMContentLoaded", () => {
    initialiseAndSetupDataTable();
    setupRegistrationsTableInputsAndButtons();
    // Delete multiple dialog setup
    deleteCheckedButton.addEventListener("click", () => {
        deleteMultipleDialog.querySelector(".num-to-delete").textContent =
            resourcesTableBody.querySelectorAll(
                "input[type='checkbox']:checked",
            ).length;
    });
    setupDialog(
        deleteMultipleDialog,
        [deleteMultipleDialog.querySelector(".btn-close")],
        [deleteCheckedButton],
    );
    deleteMultipleDialog.addEventListener("close", (e) => {
        const returnValue = deleteMultipleDialog.returnValue;
        if (returnValue === "cancel" || returnValue === "") {
            return;
        }
        form.submit();
    });
});

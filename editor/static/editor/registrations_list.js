import { setupDialog } from "/static/dialog.js";

const form = document.getElementById("registration-deletion-form");
const registrationsTableBody = document.querySelector(
    "#registrations-table tbody",
);
const deleteCheckedButton = document.getElementById("delete-checked-btn");
const numCheckedElement = document.getElementById("num-checked");

const deleteDialog = document.querySelector("#delete-dialog");
const deleteMultipleDialog = document.querySelector("#delete-multiple-dialog");

// DataTables setup
function initialiseDataTable() {
    DataTable.datetime("dd/MM/yyyy, HH:mm:ss");
    const dataTable = new DataTable("#registrations-table", {
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
    return registrationsTableBody.querySelectorAll(
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
        "#registrations-table thead input[type='checkbox']",
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
    const tableRows = registrationsTableBody.querySelectorAll("tr");
    tableRows.forEach((tr) => {
        // Select row checkbox
        const checkbox = tr.querySelector("input[type='checkbox']");
        setupRegistrationsTableCheckboxStyling(checkbox);
        checkbox.addEventListener("input", () => {
            updateDeleteCheckedButtonState(getAllSelectedRows().length);
        });
        checkbox.setAttribute("name", "registration_ids_to_delete");
        const registrationId = tr.dataset.registrationId;
        if (!registrationId) {
            return;
        }
        checkbox.setAttribute("value", registrationId);
        // Delete row button
        const deleteButton = tr.querySelector(".delete-btn");
        deleteButton.addEventListener("click", () => {
            deleteDialog
                .querySelector(".confirm-btn")
                .setAttribute("value", tr.dataset.registrationId);

            deleteDialog.querySelector(".dialog-id-to-delete").textContent =
                tr.dataset.registrationId;
        });
    });
    // Delete dialog setup
    const deleteButtons =
        registrationsTableBody.querySelectorAll(".delete-btn");
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
        hiddenInput.name = "registration_ids_to_delete";
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
            registrationsTableBody.querySelectorAll(
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

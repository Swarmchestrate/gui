const form = document.getElementById("registration-deletion-form");
const registrationsTableBody = document.querySelector(
    "#registrations-table tbody",
);
const deleteCheckedButton = document.getElementById("delete-checked-btn");
const numCheckedElement = document.getElementById("num-checked");

// DataTables setup
function initialiseDataTable() {
    const dataTable = new DataTable("#registrations-table", {
        columnDefs: [
            {
                render: DataTable.render.select(),
                target: 0,
            },
        ],
        select: {
            style: "os",
            selector: "td:first-child",
        },
        order: [[1, "asc"]],
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
            const isConfirmed = confirm(
                "Are you sure you want to delete this registration?",
            );
            if (!isConfirmed) {
                return;
            }
            const hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "registration_ids_to_delete";
            hiddenInput.value = deleteButton.dataset.registrationId;
            form.appendChild(hiddenInput);
            form.submit();
        });
    });
}

window.addEventListener("DOMContentLoaded", () => {
    initialiseAndSetupDataTable();
    setupRegistrationsTableInputsAndButtons();
    deleteCheckedButton.addEventListener("click", () => {
        const isConfirmed = confirm(
            "Are you sure you want to delete the selected registrations?",
        );
        if (!isConfirmed) {
            return;
        }
        form.submit();
    });
});

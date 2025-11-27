import { setupDialog } from "/static/dialog.js";

const form = document.getElementById("resource-deletion-form");
const deleteCheckedButton = document.getElementById("delete-checked-btn");
const numCheckedElement = document.getElementById("num-checked");

function setupMultiResourceDeletionDialog(dataTable) {
    const deleteMultipleDialog = document.querySelector(
        "#delete-multiple-dialog",
    );
    // Multi delete dialog content is updated by "delete selected (X)"
    // button.
    deleteCheckedButton.addEventListener("click", () => {
        deleteMultipleDialog.querySelector(".num-to-delete").textContent =
            getAllSelectedRows(dataTable).length;
    });
    // Multi delete dialog is updated by "delete selected (X)" button.
    setupDialog(
        deleteMultipleDialog,
        [deleteMultipleDialog.querySelector(".btn-close")],
        [deleteCheckedButton],
    );
    // Multi delete dialog submits multi delete form when closed.
    deleteMultipleDialog.addEventListener("close", (e) => {
        const returnValue = deleteMultipleDialog.returnValue;
        if (returnValue === "cancel" || returnValue === "") {
            return;
        }
        form.submit();
    });
}

function getAllSelectedRows(dataTable) {
    return dataTable.rows(".selected").nodes();
}

function updateDeleteCheckedButtonState(numChecked) {
    numCheckedElement.textContent = numChecked;
    if (numChecked === 0) {
        return deleteCheckedButton.classList.add("invisible");
    }
    return deleteCheckedButton.classList.remove("invisible");
}

function setupResourcesTableCheckboxStyling(selectAllRowsCheckbox, dataTable) {
    selectAllRowsCheckbox.classList.add("form-check-input");
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((row) => {
        const checkbox = row.querySelector("input[type='checkbox']");
        return checkbox.classList.add("form-check-input");
    });
}

export function setupMultiResourceDeletion(dataTable) {
    const selectAllRowsCheckbox = document.querySelector(
        "#resources-table thead input[type='checkbox']",
    );
    selectAllRowsCheckbox.addEventListener("input", () => {
        // Small timeout added before updating delete checked
        // button state as number of selected rows doesn't
        // update straight away.
        window.setTimeout(() => {
            updateDeleteCheckedButtonState(
                getAllSelectedRows(dataTable).length,
            );
        }, 25);
    });
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((tr) => {
        // Select row checkbox
        const checkbox = tr.querySelector("input[type='checkbox']");
        // Delete selected (X) button is updated when checkbox
        // is clicked.
        checkbox.addEventListener("input", () => {
            updateDeleteCheckedButtonState(
                getAllSelectedRows(dataTable).length,
            );
        });
        // Set checkbox attributes as these are added dynamically
        // when setting up the DataTable.
        checkbox.setAttribute("name", "resource_ids_to_delete");
        const resourceId = tr.dataset.resourceId;
        if (!resourceId) {
            return;
        }
        checkbox.setAttribute("value", resourceId);
    });
    // Apply Bootstrap styling to checkboxes.
    setupResourcesTableCheckboxStyling(selectAllRowsCheckbox, dataTable);
    // Set up multi delete dialog.
    setupMultiResourceDeletionDialog(dataTable);
}

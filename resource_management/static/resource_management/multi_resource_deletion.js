import { setupDialog } from "/static/dialog.js";

function setupMultiResourceDeletionDialog(
    dataTable,
    deleteCheckedButton,
    form
) {
    const dialogId = deleteCheckedButton.dataset.dialogId;
    const deleteMultipleDialog = document.querySelector(
        `#${dialogId}`,
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

function updateDeleteCheckedButtonState(deleteCheckedButton, numChecked) {
    deleteCheckedButton.querySelector(".num-checked").textContent = numChecked;
    if (numChecked === 0) {
        return deleteCheckedButton.classList.add("d-none");
    }
    return deleteCheckedButton.classList.remove("d-none");
}

export function setupMultiResourceDeletion(tableId, dataTable) {
    const deleteCheckedButton = document.querySelector(
        `button.delete-checked-btn[data-table-id="${tableId}"]`
    );
    if (!deleteCheckedButton) return;
    const tableSelector = `#${tableId}`;
    document.querySelector(
        `${tableSelector} thead input[type='checkbox']`
    ).addEventListener("input", () => {
        // Small timeout added before updating delete checked
        // button state as number of selected rows doesn't
        // update straight away.
        window.setTimeout(() => {
            updateDeleteCheckedButtonState(
                deleteCheckedButton,
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
                deleteCheckedButton,
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
    // Set up multi delete dialog.
    const formId = deleteCheckedButton.dataset.formId;
    const form = document.querySelector(`#${formId}`);
    setupMultiResourceDeletionDialog(
        dataTable,
        deleteCheckedButton,
        form
    );
}

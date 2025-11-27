import { setupDialog } from "/static/dialog.js";

const form = document.getElementById("resource-deletion-form");
const deleteDialog = document.querySelector("#delete-dialog");

export function setupIndividualResourceDeletion(dataTable) {
    // Delete buttons update delete dialog content when clicked.
    const dataTableRows = dataTable.rows().nodes().toArray();
    const deleteButtons = [];
    dataTableRows.forEach((tr) => {
        const deleteButton = tr.querySelector(".delete-btn");
        deleteButton.addEventListener("click", () => {
            deleteDialog
                .querySelector(".confirm-btn")
                .setAttribute("value", tr.dataset.resourceId);

            deleteDialog.querySelector(".dialog-id-to-delete").textContent =
                tr.dataset.resourceId;
        });
        deleteButtons.push(deleteButton);
    });
    // Delete buttons open delete dialog when clicked.
    setupDialog(
        deleteDialog,
        [deleteDialog.querySelector(".btn-close")],
        deleteButtons,
    );
    // Delete dialog submits individual deletion form
    // when cloed.
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

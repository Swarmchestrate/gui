import { setupDialog } from "/static/dialog.js";

const deleteDialog = document.querySelector("#delete-dialog");

export function setupIndividualResourceDeletion(dataTable) {
    // Delete buttons update delete dialog content when clicked.
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((tr) => {
        const deleteButton = tr.querySelector(".delete-btn");
        const deleteDialog = document.querySelector(
            `#${deleteButton.dataset.dialogId}`,
        );
        // Open delete dialog when button clicked.
        setupDialog(
            deleteDialog,
            [
                deleteDialog.querySelector(".btn-close"),
                deleteDialog.querySelector("button[value='cancel']"),
            ],
            [deleteButton],
        );
    });
}

import { initialiseAndSetupDataTable } from "/static/resource_management/base_resource_list.js";
import { setupDialog } from "/static/dialog.js";

const newDialog = document.querySelector("#new-dialog");

function setupNewDialog() {
    setupDialog(
        newDialog,
        [newDialog.querySelector(".btn-close")],
        [document.querySelector("#new-dialog-button")],
    );
}

function setupUpdateDialogs(dataTable) {
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((tr) => {
        const updateButtons = Array.from(tr.querySelectorAll(".edit-btn"));
        const updateDialogId = updateButtons[0].dataset.dialogId;
        const updateDialog = document.querySelector(
            `#${updateDialogId}`,
        );
        // Open update dialog when button clicked.
        setupDialog(
            updateDialog,
            [
                updateDialog.querySelector(".btn-close"),
            ],
            updateButtons,
        );
    });
}

export function setupIndividualResourceDeletion(dataTable) {
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

// Table row setup
window.addEventListener("DOMContentLoaded", () => {
    setupNewDialog();
    const dataTable = initialiseAndSetupDataTable([
        "checkbox",
        "table_name",
        "column_name",
        "date_created",
        "date_updated",
        "actions",
    ]);
    setupUpdateDialogs(dataTable);
});
import { setupDialog } from "/static/dialog.js";
import { initialiseAndSetupDataTable } from "/static/resource_management/data_table_setup.js";

function setupTableRowNewDialogs(dataTable) {
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((tr) => {
        const newButton = tr.querySelector(".new-btn");
        if (!newButton) return;
        const newDialogId = newButton.dataset.dialogId;
        const newDialog = document.querySelector(
            `#${newDialogId}`,
        );
        if (!newDialog) {
            return console.error(`New resource dialog #${newButton.dataset.dialogId} not found.`);
        }
        // Open update dialog when button clicked.
        setupDialog(
            newDialog,
            [
                newDialog.querySelector(".btn-close"),
            ],
            [newButton],
        );
    });
}

function setupTableRowUpdateDialogs(dataTable) {
    const dataTableRows = dataTable.rows().nodes().toArray();
    dataTableRows.forEach((tr) => {
        const updateButtons = Array.from(tr.querySelectorAll(".edit-btn"));
        if (updateButtons.length === 0) return;
        const updateDialogId = updateButtons[0].dataset.dialogId;
        const updateDialog = document.querySelector(
            `#${updateDialogId}`,
        );
        if (!updateDialog) {
            return console.error(`Update dialog #${updateButtons[0].dataset.dialogId} not found.`);
        }
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

function setupResourcesTable(tableElement) {
    const dataTable = initialiseAndSetupDataTable(
        tableElement.id,
        [
            "checkbox",
            "column_name",
            "title",
            "actions",
        ],
        {
            selectableCondition: (rowData, tr) => {
                return Boolean(tr.querySelector("td:nth-child(2) button"));
            }
        }
    );
    setupTableRowNewDialogs(dataTable);
    setupTableRowUpdateDialogs(dataTable);
}

// Table row setup
window.addEventListener("DOMContentLoaded", () => {
    const resourcesTables = Array.from(document.querySelectorAll(".resources-table"));
    resourcesTables.forEach(tableElement => {
        setupResourcesTable(tableElement);
    });
});
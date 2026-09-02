import { setupDialog } from "/static/dialog.js";
import { initialiseAndSetupDataTable } from "/static/resource_management/data_table_setup.js";

function setupTableRowNewDialogs(dataTable) {
    const newResourceTemplateUrl = JSON.parse(document.querySelector("#new-resource-template-url").textContent);
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
        const newDialogForm = newDialog.querySelector("form");
        const newDialogFieldNamePlaceholder = newDialog.querySelector(".field-name");
        const tableName = newButton.dataset.tableName;
        const columnName = newButton.dataset.columnName;
        const newResourceUrl = `${
            newResourceTemplateUrl.replace("__table_name__", tableName).replace("__column_name__", columnName)
        }?table_name=${encodeURIComponent(tableName)}`;
        newButton.addEventListener("click", () => {
            newDialogFieldNamePlaceholder.textContent = columnName;
            newDialogForm.setAttribute("action", newResourceUrl);
        });
        // Open update dialog when button clicked.
        setupDialog(
            newDialog,
            [
                newDialog.querySelector(".btn-close"),
            ],
            [newButton],
        );
        // Form is reset if changes haven't been submitted, as carrying over changes
        // may cause confusion when going to edit another field. If changes have been made,
        // the form is reset after it has been submitted, so an empty form isn't submitted.
        newDialog.addEventListener("close", () => {
            newDialogForm.reset();
        });
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
import { setupDialog } from "/static/dialog.js";
import { htmlToNode } from "/static/editor/utils.js";
import { initialiseAndSetupDataTable } from "/static/resource_management/data_table_setup.js";

const newDialog = document.querySelector("#new-dialog");
const getColumnsForTableUrlBase = JSON.parse(
    document.querySelector("#get-columns-url-template").textContent
);
const spinnerElement = htmlToNode('<span class="spinner-border spinner-border-sm ms-2" aria-hidden="true"></span>');


async function getColumnsForTable(tableName) {
    const getColumnsForTableUrl = getColumnsForTableUrlBase.replace(
        "__table_name__",
        tableName
    );
    const response = await fetch(getColumnsForTableUrl, {
        "method": "GET",
    });
    if (!response.ok) {
        throw new Error("A problem occurred whilst attempting to get the column names for a table.");
    }
    const responseContent = await response.json();
    return responseContent.columns;

} 

function updateColumnNameSelect(columnNameSelect, columnNames) {
    const blankOption = document.createElement("OPTION");
    blankOption.value = "";
    const options = columnNames.map(columnName => {
        const optionElement = document.createElement("OPTION");
        optionElement.value = columnName;
        optionElement.textContent = columnName;
        return optionElement;
    });
    columnNameSelect.replaceChildren(blankOption, ...options);
    columnNameSelect.disabled = false;
}

async function refreshColumnNames(tableName, columnNameSelect) {
    const labelElement = document.querySelector(`label[for="${columnNameSelect.id}"]`);
    labelElement.insertAdjacentElement("afterend", spinnerElement);
    columnNameSelect.disabled = true;
    try {
        const columnNames = await getColumnsForTable(tableName);
        updateColumnNameSelect(columnNameSelect, columnNames);
    } catch (error) {
        console.error(error);
    }
    spinnerElement.remove();
}

async function setupNewDialog() {
    setupDialog(
        newDialog,
        [newDialog.querySelector(".btn-close")],
        [document.querySelector("#new-dialog-button")],
    );
    const tableNameSelect = newDialog.querySelector("select[name='table_name']");
    const columnNameSelect = newDialog.querySelector("select[name='column_name']");
    if (!tableNameSelect || !columnNameSelect) return;
    if (tableNameSelect.value) {
        await refreshColumnNames(tableNameSelect.value, columnNameSelect);
    }
    tableNameSelect.addEventListener("change", async () => {
        await refreshColumnNames(tableNameSelect.value, columnNameSelect);
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

function setupDataTableForTabPane(tabPane) {
    const tableElement = tabPane.querySelector("table");
    const dataTable = initialiseAndSetupDataTable(
        tableElement.id,
        [
            "checkbox",
            "column_name",
            "title",
            "date_created",
            "date_updated",
            "actions",
        ]
    );
    setupTableRowUpdateDialogs(dataTable);
}

// Table row setup
window.addEventListener("DOMContentLoaded", async () => {
    // const activeTabPane = document.querySelector("#table-nav-tabContent .tab-pane.active");
    // setupDataTableForTabPane(activeTabPane);
    const tabPanes = Array.from(document.querySelectorAll("#table-nav-tabContent .tab-pane"));
    tabPanes.forEach(tabPane => {
        setupDataTableForTabPane(tabPane);
    });
    const bsTab = new bootstrap.Tab("#table-nav-tab");
    // await setupNewDialog();
});
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

function setupDataTableForTabPane(tabPane) {
    const tableElement = tabPane.querySelector("table");
    const dataTable = initialiseAndSetupDataTable(
        tableElement.id,
        [
            "checkbox",
            "column_name",
            "title",
            "actions",
        ]
    );
    setupTableRowNewDialogs(dataTable);
    setupTableRowUpdateDialogs(dataTable);
}

function saveCurrentTabInPageUrlParams(event) {
    const selectedTabPaneButton = event.target;
    const selectedTableName =
        selectedTabPaneButton.dataset.tableName;
    if ("URLSearchParams" in window) {
        const url = new URL(window.location);
        url.searchParams.set("table_name", selectedTableName);
        history.pushState(null, "", url);
    }
}

function appendCurrentTabToFormActionAndSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formAction = form.getAttribute("action");
    if (!formAction) return form.submit();
    const pageUrl = new URL(window.location);
    const tableNameInPageUrl = pageUrl.searchParams.get("table_name");
    if (tableNameInPageUrl) {
        const newFormUrl = new URL(
            formAction,
            window.location.origin
        );
        newFormUrl.searchParams.set("table_name", tableNameInPageUrl)
        form.setAttribute("action", newFormUrl);
    }
    return form.submit();
}

// Table row setup
window.addEventListener("DOMContentLoaded", () => {
    const forms = Array.from(document.querySelectorAll(
        ".multi-resource-deletion-form, #dialogs form:not([method='dialog'])"
    ));
    forms.forEach(form => {
        form.addEventListener("submit", appendCurrentTabToFormActionAndSubmit);
    });
    const tabPanes = Array.from(document.querySelectorAll("#table-nav-tabContent .tab-pane"));
    tabPanes.forEach(tabPane => {
        setupDataTableForTabPane(tabPane);
    });
    // Set up tabs to save the current tab in the page's URL
    // params after switching.
    const tabPaneButtons = Array.from(
        document.querySelectorAll("#table-nav-tab button[data-bs-toggle='tab']"),
    );
    tabPaneButtons.forEach((tabPaneButton) => {
        tabPaneButton.addEventListener("shown.bs.tab", saveCurrentTabInPageUrlParams);
    });
});
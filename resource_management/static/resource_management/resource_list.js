import { initialiseAndSetupDataTable } from "/static/resource_management/data_table_setup.js";

// Table row setup
window.addEventListener("DOMContentLoaded", () => {
    const tableElementId = "resources-table";
    initialiseAndSetupDataTable(
        tableElementId,
        [
            "checkbox",
            "id",
            "date_created",
            "date_updated",
            "actions",
        ],
        {
            createdAtColumnIndex: 2,
            updatedAtColumnIndex: 3,
        }
    );
    document.querySelectorAll("[data-bs-toggle='tooltip']").forEach(
        (tooltipTriggerElement) => new bootstrap.Tooltip(tooltipTriggerElement)
    );
});

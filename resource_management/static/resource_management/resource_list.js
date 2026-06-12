import { initialiseAndSetupDataTable } from "/static/resource_management/base_resource_list.js";

// Table row setup
window.addEventListener("DOMContentLoaded", () => {
    initialiseAndSetupDataTable([
        "checkbox",
        "id",
        "date_created",
        "date_updated",
        "actions",
    ]);
});

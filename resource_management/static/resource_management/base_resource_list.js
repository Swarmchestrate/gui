import { setupIndividualResourceDeletion } from "/static/resource_management/resource_deletion.js";
import { setupMultiResourceDeletion } from "/static/resource_management/multi_resource_deletion.js";

// DataTables setup
function initialiseDataTable(columnNames) {
    DataTable.datetime("dd/MM/yyyy, HH:mm:ss");
    const dataTable = new DataTable("#resources-table", {
        columnDefs: [
            {
                orderable: false,
                render: DataTable.render.select(),
                target: 0,
            },
        ],
        columns: columnNames.map(columnName => { name: columnName }),
        select: {
            style: "os",
            selector: "td:first-child",
        },
        order: {
            name: "date_updated",
            dir: "desc",
        },
    });
    return dataTable;
}

function setupDataTableEventListeners(dataTable) {
    dataTable.on("select", (e, dt, type, indexes) => {
        if (type !== "row") {
            return;
        }
        const selected = dataTable.rows(indexes).nodes().toArray();
        selected.forEach((row) => {
            row.classList.add("table-active");
        });
    });

    dataTable.on("deselect", (e, dt, type, indexes) => {
        if (type !== "row") {
            return;
        }
        const deselected = dataTable.rows(indexes).nodes().toArray();
        deselected.forEach((row) => {
            row.classList.remove("table-active");
        });
    });
}

export function initialiseAndSetupDataTable(columnNames) {
    const dataTable = initialiseDataTable(columnNames);
    setupDataTableEventListeners(dataTable);
    setupIndividualResourceDeletion(dataTable);
    setupMultiResourceDeletion(dataTable);
    return dataTable;
}

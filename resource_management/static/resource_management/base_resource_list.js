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
        order: [[3, "desc"]],
        language: {
            search: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16" role="img" aria-label="Search" style="transform: translateY(-0.125em);">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                    </svg>`,
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

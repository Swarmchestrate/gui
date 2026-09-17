/**
 * Keeps a key/value field's hidden JSON in step with its visible rows.
 *
 * Listens once at the document rather than on each field, so rows inside
 * dialogs injected after the page loads - and dialogs cloned for rows added
 * later - work without anything having to find and set them up.
 */
function syncField(field) {
    const map = {};
    for (const row of field.querySelectorAll(".key-value-row")) {
        const key = row.querySelector("[data-kv='key']").value.trim();
        if (!key) {
            // A row still being filled in has no name to key it by.
            continue;
        }
        map[key] = row.querySelector("[data-kv='value']").value;
    }
    field.querySelector("input[type='hidden']").value = JSON.stringify(map);
}

export function setupKeyValueFields() {
    if (document.keyValueFieldsReady) {
        return;
    }
    document.keyValueFieldsReady = true;

    document.addEventListener("click", (event) => {
        const field = event.target.closest(".key-value-field");
        if (!field) {
            return;
        }
        if (event.target.closest(".add-btn")) {
            const row = field.querySelector("template").content.firstElementChild.cloneNode(true);
            field.querySelector("ul").append(row);
            row.querySelector("[data-kv='key']").focus();
        } else if (event.target.closest(".delete-btn")) {
            event.target.closest(".key-value-row").remove();
            syncField(field);
        }
    });

    document.addEventListener("input", (event) => {
        const field = event.target.closest(".key-value-field");
        if (field && event.target.matches("[data-kv]")) {
            syncField(field);
        }
    });
}

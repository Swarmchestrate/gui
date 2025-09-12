const form = document.getElementById("registration-deletion-form");
const registrationsTableBody = document.querySelector(
    "#registrations-table tbody",
);
const tableRows = registrationsTableBody.querySelectorAll("tr");
const deleteCheckedButton = document.getElementById("delete-checked-btn");
const numCheckedElement = document.getElementById("num-checked");
const selectAllCheckbox = document.getElementById("select-all-registrations");

function updateSelectAllCheckboxState() {
    const numChecked = registrationsTableBody.querySelectorAll(
        "input[type='checkbox']:checked",
    ).length;
    if (numChecked === 0) {
        selectAllCheckbox.indeterminate = false;
        return (selectAllCheckbox.checked = false);
    }
    const allChecked = numChecked === tableRows.length;
    if (allChecked) {
        selectAllCheckbox.indeterminate = false;
        return (selectAllCheckbox.checked = true);
    }
    return (selectAllCheckbox.indeterminate = true);
}

function updateDeleteCheckedButtonState() {
    const numChecked = registrationsTableBody.querySelectorAll(
        "input[type='checkbox']:checked",
    ).length;
    numCheckedElement.textContent = numChecked;
    if (numChecked === 0) {
        return deleteCheckedButton.classList.add("invisible");
    }
    return deleteCheckedButton.classList.remove("invisible");
}

function setupSelectableTableRows() {
    tableRows.forEach((tableRow) => {
        const checkbox = tableRow.querySelector("input[type='checkbox']");
        checkbox.addEventListener("input", () => {
            updateSelectAllCheckboxState();
            updateDeleteCheckedButtonState();
            if (checkbox.checked) {
                return tableRow.classList.add("table-active");
            }
            return tableRow.classList.remove("table-active");
        });

        const deleteButton = tableRow.querySelector(".delete-btn");
        deleteButton.addEventListener("click", () => {
            const isConfirmed = confirm(
                "Are you sure you want to delete this registration?",
            );
            if (!isConfirmed) {
                return;
            }
            const hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "registration_ids_to_delete";
            hiddenInput.value = deleteButton.dataset.registrationId;
            form.appendChild(hiddenInput);
            form.submit();
        });
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setupSelectableTableRows();
    updateDeleteCheckedButtonState();
    deleteCheckedButton.addEventListener("click", () => {
        const isConfirmed = confirm(
            "Are you sure you want to delete the selected registrations?",
        );
        if (!isConfirmed) {
            return;
        }
        form.submit();
    });
    selectAllCheckbox.addEventListener("input", () => {
        tableRows.forEach((tableRow) => {
            const checkbox = tableRow.querySelector("input[type='checkbox']");
            checkbox.checked = selectAllCheckbox.checked;
            updateDeleteCheckedButtonState();
            if (selectAllCheckbox.checked) {
                return tableRow.classList.add("table-active");
            }
            return tableRow.classList.remove("table-active");
        });
    });
});

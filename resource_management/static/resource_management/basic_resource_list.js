import { setupDialog } from "/static/dialog.js";

const newDialog = document.querySelector("#new-dialog");
const updateDialogs = document.querySelectorAll(".update-dialog[id]");

window.addEventListener("DOMContentLoaded", () => {
    setupDialog(
        newDialog,
        [newDialog.querySelector(".btn-close")],
        [document.querySelector("#new-dialog-button")],
    );
    updateDialogs.forEach((updateDialog) => {
        const openButtons = document.querySelectorAll(
            `.edit-btn[data-dialog-id="${updateDialog.id}"]`,
        );
        setupDialog(
            updateDialog,
            [updateDialog.querySelector(".btn-close")],
            Array.from(openButtons),
        );
    });
});

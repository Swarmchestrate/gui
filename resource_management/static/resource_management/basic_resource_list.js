import { setupDialog } from "/static/dialog.js";

const newDialog = document.querySelector("#new-dialog");
const updateDialogOpenButtons = document.querySelectorAll(
    ".edit-btn[data-dialog-id]",
);

window.addEventListener("DOMContentLoaded", () => {
    setupDialog(
        newDialog,
        [newDialog.querySelector(".btn-close")],
        [document.querySelector("#new-dialog-button")],
    );
    updateDialogOpenButtons.forEach((button) => {
        const updateDialog = document.querySelector(
            `#${button.dataset.dialogId}`,
        );
        setupDialog(
            updateDialog,
            [updateDialog.querySelector(".btn-close")],
            [button],
        );
    });
});

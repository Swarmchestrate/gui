import { setupDialog } from "/static/dialog.js";

const newDialogButtons = document.querySelectorAll(".new-dialog-btn");
// const newDialog = document.querySelector("#new-dialog");
const updateDialogs = document.querySelectorAll(".update-dialog[id]");

window.addEventListener("DOMContentLoaded", () => {
    Array.from(newDialogButtons).forEach((button) => {
        const newDialog = document.querySelector(`#${button.dataset.dialogId}`);
        setupDialog(
            newDialog,
            [newDialog.querySelector(".btn-close")],
            [button],
        );
    });
});

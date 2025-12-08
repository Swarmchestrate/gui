import { setupDialog } from "/static/dialog.js";

const dialogButtons = document.querySelectorAll("button[data-dialog-id]");

window.addEventListener("DOMContentLoaded", () => {
    Array.from(dialogButtons).forEach((dialogButton) => {
        const dialogElement = document.querySelector(
            `#${dialogButton.dataset.dialogId}`,
        );
        setupDialog(
            dialogElement,
            [dialogElement.querySelector(".btn-close")],
            [dialogButton],
        );
    });
});

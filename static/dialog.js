export function addShowButtonToDialog(showButton, dialog, closeButton) {
    showButton.addEventListener("click", () => {
        dialog.removeAttribute("inert");
        dialog.showModal();
        // Close button should autofocus with
        // dialog, but doesn't in Safari for
        // some reason.
        if (typeof closeButton === "undefined") {
            closeButton = dialog.querySelector(".btn-close");
        }
        if (!closeButton) {
            return;
        }
        closeButton.focus();
    });
}

export function setupDialog(dialog, closeButton, showButtons, options) {
    if (typeof options === "undefined") {
        options = {
            closeOnBackdropClick: true,
        };
    }
    // Light dismiss - allows dialog to be closed
    // by clicking on the backdrop.
    if (options.closeOnBackdropClick) {
        dialog.addEventListener("click", () => {
            dialog.close();
        });
    }

    dialog
        .querySelector(".dialog-content")
        .addEventListener("click", (event) => {
            event.stopPropagation();
        });

    closeButton.addEventListener("click", () => {
        dialog.close("");
    });

    dialog.addEventListener("close", () => {
        // When the dialog is closed, set the
        // inert attribute to true so that it's
        // not focusable by keyboard/assistive
        // technologies.
        dialog.setAttribute("inert", "");
    });

    showButtons.forEach((showButton) => {
        addShowButtonToDialog(showButton, dialog, closeButton);
    });
}

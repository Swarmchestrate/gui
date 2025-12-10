export function addShowButtonToDialog(showButton, dialog, closeButtons) {
    showButton.addEventListener("click", () => {
        dialog.removeAttribute("inert");
        dialog.showModal();
        // Close button should autofocus with
        // dialog, but doesn't in Safari for
        // some reason.
        let closeButton = dialog.querySelector(".btn-close");
        if (closeButtons.length) {
            closeButton = closeButtons[0];
        }
        if (!closeButton) {
            return;
        }
        closeButton.focus();
    });
}

export function setupDialog(dialog, closeButtons, showButtons, options) {
    if (typeof options === "undefined") {
        options = {
            lightDismiss: true,
        };
    }
    // Light dismiss - allows dialog to be closed
    // by clicking on the backdrop.
    if (options.lightDismiss) {
        dialog.addEventListener("click", () => {
            dialog.close();
        });
    }

    dialog
        .querySelector(".dialog-header")
        .addEventListener("click", (event) => {
            event.stopPropagation();
        });

    dialog
        .querySelector(".dialog-content")
        .addEventListener("click", (event) => {
            event.stopPropagation();
        });

    dialog
        .querySelector(".dialog-footer")
        .addEventListener("click", (event) => {
            event.stopPropagation();
        });

    closeButtons.forEach((closeButton) => {
        closeButton.addEventListener("click", () => {
            dialog.close("");
        });
    });

    dialog.addEventListener("close", () => {
        // When the dialog is closed, set the
        // inert attribute to true so that it's
        // not focusable by keyboard/assistive
        // technologies.
        dialog.setAttribute("inert", "");
    });

    showButtons.forEach((showButton) => {
        addShowButtonToDialog(showButton, dialog, closeButtons);
    });
}

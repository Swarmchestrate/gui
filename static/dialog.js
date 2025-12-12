export class Dialog {
    constructor(dialog, closeButtons, showButtons, options) {
        this.dialog = dialog;
        this.mainCloseButton = closeButtons[0];
        this.closeButtons = closeButtons;
        this.showButtons = showButtons;
        if (typeof options !== "object") {
            options = {};
        }
        if (!("lightDismiss" in options)) {
            options.lightDismiss = true;
        }
        this.options = options;
        this.setup();
    }

    setup() {
        // Light dismiss - allows dialog to be closed
        // by clicking on the backdrop.
        if (this.options.lightDismiss) {
            this.dialog.addEventListener("click", () => {
                this.closeWithoutSaving();
            });
            this.dialog
                .querySelector(".dialog-header")
                .addEventListener("click", (event) => {
                    event.stopPropagation();
                });
            this.dialog
                .querySelector(".dialog-content")
                .addEventListener("click", (event) => {
                    event.stopPropagation();
                });
            this.dialog
                .querySelector(".dialog-footer")
                .addEventListener("click", (event) => {
                    event.stopPropagation();
                });
        }
        this.closeButtons.forEach((closeButton) => {
            closeButton.addEventListener("click", () => {
                this.closeWithoutSaving();
            });
        });

        this.dialog.addEventListener("close", () => {
            // When the dialog is closed, set the
            // inert attribute to true so that it's
            // not focusable by keyboard/assistive
            // technologies.
            this.dialog.setAttribute("inert", "");
        });
        this.showButtons.forEach((showButton) => {
            this.addShowButton(showButton);
        });
    }

    closeWithoutSaving() {
        this.dialog.close("");
    }

    addShowButton(showButton) {
        showButton.addEventListener("click", () => {
            this.dialog.removeAttribute("inert");
            this.dialog.showModal();
            // Close button should autofocus with
            // dialog, but doesn't in Safari for
            // some reason.
            this.mainCloseButton.focus();
        });
    }
}

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
    if (typeof options !== "object") {
        options = {};
    }
    if (!("lightDismiss" in options)) {
        options.lightDismiss = true;
    }
    // Light dismiss - allows dialog to be closed
    // by clicking on the backdrop.
    if (options.lightDismiss) {
        dialog.addEventListener("click", () => {
            dialog.close();
        });
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
    }

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

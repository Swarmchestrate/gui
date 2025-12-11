import { FormDialog } from "/static/editor/form_dialog.js";

const oneToOneFields = Array.from(
    document.querySelectorAll(".one-to-one-field"),
);

class OneToOneField {
    constructor(oneToOneField) {
        this.oneToOneField = oneToOneField;
        this.setupClassFields();
        this.setupDialogs();
    }

    setupClassFields() {
        // New dialog button
        this.newDialogButton = this.oneToOneField.querySelector(
            "button.new-dialog-btn[data-dialog-id]",
        );
        this.newDialogElement = document.querySelector(
            `#${this.newDialogButton.dataset.dialogId}`,
        );
        this.newDialogForm = this.newDialogElement.querySelector("form");
        // Update dialog button
        this.updateDialogButton = this.oneToOneField.querySelector(
            "button.update-dialog-btn[data-dialog-id]",
        );
        this.updateDialogElement = document.querySelector(
            `#${this.updateDialogButton.dataset.dialogId}`,
        );
        this.updateDialogForm = this.updateDialogElement.querySelector("form");
        // Delete dialog button
        this.deleteDialogButton = this.oneToOneField.querySelector(
            "button.delete-dialog-btn[data-dialog-id]",
        );
        this.deleteDialogElement = document.querySelector(
            `#${this.deleteDialogButton.dataset.dialogId}`,
        );
        this.deleteDialogForm = this.deleteDialogElement.querySelector("form");
    }

    setupDialogs() {
        // Setup dialogs
        this.setupNewDialog();
        this.setupUpdateDialog();
        this.setupDeleteDialog();
    }

    setupNewDialog() {
        new FormDialog(
            this.newDialogElement,
            [this.newDialogElement.querySelector(".btn-close")],
            [this.newDialogButton],
            {
                onFormSuccess: (responseData) => {
                    this.newDialogForm.reset();
                    this.newDialogButton.classList.add("d-none");
                    this.updateDialogButton.classList.remove("d-none");
                    this.deleteDialogButton.classList.remove("d-none");
                    for (const property in responseData.resource) {
                        const propertyValue = responseData.resource[property];
                        const elementForProperty =
                            this.oneToOneField.querySelector(
                                `[data-field="${property}"]`,
                            );
                        if (!elementForProperty) continue;
                        elementForProperty.textContent = propertyValue;
                        const fieldForProperty =
                            this.updateDialogForm.querySelector(
                                `[name="${property}"]`,
                            );
                        fieldForProperty.defaultValue = propertyValue;
                        if (fieldForProperty.options) {
                            for (const option of fieldForProperty.options) {
                                if (option.value !== propertyValue) {
                                    option.removeAttribute("selected");
                                    continue;
                                }
                                option.setAttribute("selected", "selected");
                            }
                        }
                        this.updateDialogForm.reset();
                    }
                    this.deleteDialogForm.querySelector(
                        "[name='resource_id_to_delete']",
                    ).value = responseData.resource.pk;
                },
            },
            this.newDialogForm,
        );
    }

    setupUpdateDialog() {
        new FormDialog(
            this.updateDialogElement,
            [this.updateDialogElement.querySelector(".btn-close")],
            [this.updateDialogButton],
            {
                onFormSuccess: (responseData) => {
                    for (const property in responseData.resource) {
                        const propertyValue = responseData.resource[property];
                        const elementForProperty =
                            this.oneToOneField.querySelector(
                                `[data-field="${property}"]`,
                            );
                        if (!elementForProperty) continue;
                        elementForProperty.textContent = propertyValue;
                        const fieldForProperty =
                            this.updateDialogForm.querySelector(
                                `[name="${property}"]`,
                            );
                        fieldForProperty.defaultValue = propertyValue;
                        if (fieldForProperty.options) {
                            for (const option of fieldForProperty.options) {
                                if (option.value !== propertyValue) {
                                    option.removeAttribute("selected");
                                    continue;
                                }
                                option.setAttribute("selected", "selected");
                            }
                        }
                        this.updateDialogForm.reset();
                    }
                },
            },
            this.updateDialogForm,
        );
    }

    setupDeleteDialog() {
        new FormDialog(
            this.deleteDialogElement,
            [this.deleteDialogElement.querySelector(".btn-close")],
            [this.deleteDialogButton],
            {
                onFormSuccess: (responseData) => {
                    this.newDialogButton.classList.remove("d-none");
                    this.updateDialogButton.classList.add("d-none");
                    this.deleteDialogButton.classList.add("d-none");
                    Array.from(
                        this.updateDialogForm.querySelectorAll(
                            "input, textarea, select",
                        ),
                    ).forEach((field) => {
                        if (
                            field.getAttribute("name") == "csrfmiddlewaretoken"
                        ) {
                            return;
                        }
                        try {
                            field.defaultValue = "";
                        } catch (error) {}
                        try {
                            field.value = "";
                        } catch (error) {}
                    });
                    this.updateDialogForm.reset();
                    Array.from(
                        this.oneToOneField.querySelectorAll("[data-field]"),
                    ).forEach((element) => {
                        element.textContent = "None";
                    });
                },
            },
            this.deleteDialogForm,
        );
    }
}

window.addEventListener("DOMContentLoaded", () => {
    oneToOneFields.forEach((oneToOneField) => {
        new OneToOneField(oneToOneField);
    });
});

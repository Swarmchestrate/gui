import { FormDialog } from "/static/editor/form_dialog.js";

let dialogsContainer;

class OneToManyField {
    constructor(oneToManyField) {
        this.oneToManyField = oneToManyField;
        this.list = oneToManyField.querySelector("ul.list-group");
        this.fieldName = oneToManyField.dataset.field;
        this.setupClassFields();
        this.setupNewDialog();
        this.setupExistingListItems();
    }

    setupClassFields() {
        // HTML template strings
        this.updateDialogHtmlTemplate = JSON.parse(
            document.querySelector(
                `#${this.fieldName}-update_dialog-form-template`,
            ).textContent,
        );
        this.deleteDialogHtmlTemplate = JSON.parse(
            document.querySelector(
                `#${this.fieldName}-delete_dialog-form-template`,
            ).textContent,
        );
        this.listItemHtmlTemplate = JSON.parse(
            document.querySelector(`#${this.fieldName}-list_item-form-template`)
                .textContent,
        );
        // New dialog button
        this.newDialogButton = this.oneToManyField.querySelector(
            "button.new-dialog-btn[data-dialog-id]",
        );
        this.newDialogElement = document.querySelector(
            `#${this.newDialogButton.dataset.dialogId}`,
        );
        this.newDialogForm = this.newDialogElement.querySelector("form");
        this.csrfMiddlewareTokenInput = this.newDialogForm
            .querySelector("input[name='csrfmiddlewaretoken']")
            .cloneNode(true);
    }

    setupNewDialog() {
        new FormDialog(
            this.newDialogElement,
            [this.newDialogElement.querySelector(".btn-close")],
            [this.newDialogButton],
            {
                onFormSuccess: (responseData) => {
                    this.newDialogForm.reset();
                    const listItem = this.setupResource(responseData.resource);
                    this.setupListItem(listItem);
                },
            },
            this.newDialogForm,
        );
    }

    setupExistingListItems() {
        const listItems = Array.from(
            this.list.querySelectorAll("li.list-group-item"),
        );
        listItems.forEach((listItem) => {
            this.setupListItem(listItem);
        });
    }

    setupListItem(listItem) {
        new OneToManyFieldListItem(listItem);
    }

    // New resource methods
    setupResource(resource) {
        const updateDialog =
            this.createUpdateDialogElementForResource(resource);
        dialogsContainer.appendChild(updateDialog);
        const deleteDialog =
            this.createDeleteDialogElementForResource(resource);
        dialogsContainer.appendChild(deleteDialog);
        const listItem = this.createListItemElementForResource(resource);
        this.list.appendChild(listItem);
        return listItem;
    }

    setupTemplateForResource(htmlTemplateString, resource) {
        const htmlTemplateStringFormatted = htmlTemplateString
            .trim()
            .replaceAll("__resource_id__", resource.pk);
        const template = document.createElement("TEMPLATE");
        template.innerHTML = htmlTemplateStringFormatted;
        return template.content.firstChild;
    }

    getCsrfMiddlewareTokenInput() {
        return this.csrfMiddlewareTokenInput.cloneNode();
    }

    createUpdateDialogElementForResource(resource) {
        const updateDialog = this.setupTemplateForResource(
            this.updateDialogHtmlTemplate,
            resource,
        );
        const updateDialogForm = updateDialog.querySelector("form");
        updateDialogForm.prepend(this.getCsrfMiddlewareTokenInput());
        for (const property in resource) {
            let propertyValue = resource[property];
            const fieldForProperty = updateDialogForm.querySelector(
                `[name="${property}"]`,
            );
            if (!fieldForProperty) continue;
            if (propertyValue === null) {
                propertyValue = "";
            }
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
        }
        updateDialogForm.reset();
        return updateDialog;
    }

    createDeleteDialogElementForResource(resource) {
        const deleteDialog = this.setupTemplateForResource(
            this.deleteDialogHtmlTemplate,
            resource,
        );
        const deleteDialogForm = deleteDialog.querySelector("form");
        deleteDialogForm.prepend(this.getCsrfMiddlewareTokenInput());
        return deleteDialog;
    }

    createListItemElementForResource(resource) {
        const listItem = this.setupTemplateForResource(
            this.listItemHtmlTemplate,
            resource,
        );
        for (const property in resource) {
            const propertyValue = resource[property];
            const elementForProperty = listItem.querySelector(
                `[data-field="${property}"]`,
            );
            if (!elementForProperty) continue;
            elementForProperty.textContent = propertyValue;
            if (!propertyValue) {
                elementForProperty.textContent = "None";
            }
        }
        return listItem;
    }
}

class OneToManyFieldListItem {
    constructor(listItem) {
        this.listItem = listItem;
        this.setupClassFields();
        this.setupDialogs();
    }

    setupClassFields() {
        // Update dialog button
        this.updateDialogButton = this.listItem.querySelector(
            "button.update-dialog-btn[data-dialog-id]",
        );
        this.updateDialogElement = document.querySelector(
            `#${this.updateDialogButton.dataset.dialogId}`,
        );
        this.updateDialogForm = this.updateDialogElement.querySelector("form");
        // Delete dialog button
        this.deleteDialogButton = this.listItem.querySelector(
            "button.delete-dialog-btn[data-dialog-id]",
        );
        this.deleteDialogElement = document.querySelector(
            `#${this.deleteDialogButton.dataset.dialogId}`,
        );
        this.deleteDialogForm = this.deleteDialogElement.querySelector("form");
    }

    removeListItem() {
        this.listItem.remove();
    }

    setupDialogs() {
        this.setupUpdateDialog();
        this.setupDeleteDialog();
    }

    setupUpdateDialog() {
        new FormDialog(
            this.updateDialogElement,
            [this.updateDialogElement.querySelector(".btn-close")],
            [this.updateDialogButton],
            {
                onFormSuccess: (responseData) => {
                    for (const property in responseData.resource) {
                        let propertyValue = responseData.resource[property];
                        const elementForProperty = this.listItem.querySelector(
                            `[data-field="${property}"]`,
                        );
                        if (!elementForProperty) continue;
                        elementForProperty.textContent = propertyValue;
                        if (!propertyValue) {
                            elementForProperty.textContent = "None";
                        }
                        const fieldForProperty =
                            this.updateDialogForm.querySelector(
                                `[name="${property}"]`,
                            );
                        if (!fieldForProperty) continue;
                        if (propertyValue === null) {
                            propertyValue = "";
                        }
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
                    }
                    this.updateDialogForm.reset();
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
                    this.removeListItem();
                },
            },
            this.deleteDialogForm,
        );
    }
}

export function initialiseOneToManyFields() {
    const oneToManyFields = Array.from(
        document.querySelectorAll(".one-to-many-field"),
    );
    dialogsContainer = document.querySelector("#dialogs");
    oneToManyFields.forEach((oneToManyField) => {
        new OneToManyField(oneToManyField);
    });
}

import { AsyncForeignKeyFieldFormHandler } from "/static/editor/async_forms.js";
import { FormDialog } from "/static/editor/form_dialog.js";
import { displayToast } from "/static/editor/toasts.js";
import { htmlToNode } from "/static/editor/utils.js";

class OneToManyFieldWithEditor {
    constructor(oneToManyField) {
        this.oneToManyField = oneToManyField;
        this.list = oneToManyField.querySelector("ul.list-group");
        this.fieldName = oneToManyField.dataset.field;
        this.setupClassFields();
        this.setupNewEditor();
        this.setupExistingListItems();
    }

    setupClassFields() {
        // Default content
        this.defaultContent = this.oneToManyField.querySelector(
            ".initial-content"
        );
        // HTML template strings
        this.updateEditorHtmlTemplate = JSON.parse(
            document.querySelector(
                `#${this.fieldName}-update_editor-form-template`,
            ).textContent,
        );
        this.emptyUpdateFormHtmlTemplate = JSON.parse(
            document.querySelector(
                `#${this.fieldName}-empty_update_form-form-template`
            ).textContent
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
        this.newEditorButton = this.oneToManyField.querySelector(
            "button.new-editor-btn[data-editor-id]",
        );
        this.newEditorElement = document.querySelector(
            `#${this.newEditorButton.dataset.editorId}`,
        );
        this.newEditorForm = document.querySelector(
            `#${this.newEditorElement.dataset.formId}`
        );
        this.csrfMiddlewareTokenInput = this.newEditorForm
            .querySelector("input[name='csrfmiddlewaretoken']")
            .cloneNode(true);
        this.resourceType = this.oneToManyField.dataset.resourceType;
    }

    setupNewEditor() {
        this.newEditorButton.addEventListener("click", () => {
            this.defaultContent.classList.add("d-none");
            this.newEditorElement.classList.remove("d-none");
        });
        const backButton = this.newEditorElement.querySelector("button[data-back-id]");
        backButton.addEventListener("click", () => {
            this.defaultContent.classList.remove("d-none");
            this.newEditorElement.classList.add("d-none");
        });
        const asyncFormHandler = new AsyncForeignKeyFieldFormHandler(this.newEditorForm, {
            onSuccess: (responseData) => {
                this.newEditorForm.reset();
                const listItem = this.setupResource(responseData.resource);
                this.setupListItem(listItem);
                displayToast(`Registered ${this.resourceType} ${responseData.resource.pk}.`);
            },
            statusButtonSelector: `button[form="${this.newEditorForm.id}"]`,
        });
        asyncFormHandler.setup();
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
        const updateEditorButton = listItem.querySelector(".update-editor-btn");
        const updateEditorElement = document.querySelector(
            `#${updateEditorButton.dataset.editorId}`
        );
        updateEditorButton.addEventListener("click", () => {
            this.defaultContent.classList.add("d-none");
            updateEditorElement.classList.remove("d-none");
        });
        const backButton = updateEditorElement.querySelector("button[data-back-id]");
        backButton.addEventListener("click", () => {
            this.defaultContent.classList.remove("d-none");
            updateEditorElement.classList.add("d-none");
        });
        new OneToManyFieldListItem(listItem, this.resourceType);
    }

    // New resource methods
    setupResource(resource) {
        const emptyUpdateForm = this.createEmptyUpdateFormElementForResource(
            resource
        );
        const fkForms = document.querySelector("#fk-forms");
        fkForms.append(emptyUpdateForm);
        const updateEditorElement =
        this.createUpdateEditorElementForResource(resource);
        this.oneToManyField.querySelector(".one-to-many-field-content").appendChild(updateEditorElement);
        const dialogs = document.querySelector("#dialogs");
        const deleteDialog =
            this.createDeleteDialogElementForResource(resource);
        dialogs.appendChild(deleteDialog);
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

    createEmptyUpdateFormElementForResource(resource) {
        const emptyUpdateForm = this.setupTemplateForResource(
            this.emptyUpdateFormHtmlTemplate,
            resource
        );
        return emptyUpdateForm;
    }

    getCsrfMiddlewareTokenInput() {
        return this.csrfMiddlewareTokenInput.cloneNode();
    }

    createUpdateEditorElementForResource(resource) {
        const updateEditor = this.setupTemplateForResource(
            this.updateEditorHtmlTemplate,
            resource,
        );
        const updateEditorForm = document.querySelector(
            `#${updateEditor.dataset.formId}`
        );
        updateEditorForm.prepend(this.getCsrfMiddlewareTokenInput());
        for (const property in resource) {
            let propertyValue = resource[property];
            const fieldForProperty = updateEditor.querySelector(
                `[name="${property}"][form="${updateEditorForm.id}"]`,
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
        updateEditorForm.reset();
        return updateEditor;
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
    constructor(listItem, resourceType) {
        this.listItem = listItem;
        this.resourceType = resourceType;
        this.setupClassFields();
        this.setupUpdateEditor();
        this.setupDeleteDialog();
    }

    setupClassFields() {
        // Update editor button
        this.updateEditorButton = this.listItem.querySelector(
            "button.update-editor-btn[data-editor-id]",
        );
        this.updateEditorElement = document.querySelector(
            `#${this.updateEditorButton.dataset.editorId}`,
        );
        this.updateEditorForm = document.querySelector(
            `#${this.updateEditorElement.dataset.formId}`
        );
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

    setupUpdateEditor() {
        const asyncFormHandler = new AsyncForeignKeyFieldFormHandler(this.updateEditorForm, {
            onSuccess: (responseData) => {
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
                        document.querySelector(
                            `[name="${property}"][form="${this.updateEditorForm.id}"]`,
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
                this.updateEditorForm.reset();
                displayToast(`Updated ${this.resourceType} ${responseData.resource.pk}.`);
            },
            statusButtonSelector: `button[form="${this.updateEditorForm.id}"]`,
        });
        asyncFormHandler.setup();
    }

    setupDeleteDialog() {
        new FormDialog(
            this.deleteDialogElement,
            [
                this.deleteDialogElement.querySelector(".btn-close"),
                this.deleteDialogElement.querySelector("button[value='cancel']"),
            ],
            [this.deleteDialogButton],
            {
                onFormSuccess: (responseData) => {
                    this.removeListItem();
                    displayToast(`Deleted ${this.resourceType} ${this.deleteDialogForm.querySelector(
                        "[name='resource_id_to_delete']"
                    ).value}.`);
                },
            },
            this.deleteDialogForm,
        );
    }
}

async function getFieldContent(fieldContentUrl) {
    const response = await fetch(
        fieldContentUrl,
        { method: "GET" },
    );
    if (!response.ok) {
        console.error(
            "Received an error whilst loading field content: ",
            response.status,
            response.statusText,
        );
    }
    let responseContent = "";
    
    // Try to extract JSON from response, first.
    let isJsonInResponse = true;
    try {
        responseContent = await response.json();
    } catch (error) {
        isJsonInResponse = false;
        console.log("response", response);
        console.error("The response was not in the expected format.");
    }

    if (isJsonInResponse) {
        return responseContent;
    }

    // Inspect text from the response, in
    // case something has gone wrong.
    try {
        const content = await response.text();
        console.log("content", content);
    } catch (error) {
        console.error("Could not extract text from the response.");
    }
    return console.error(
        "Could not load field content due to an error."
    );
}

export async function loadOneToManyFields() {
    const oneToManyFields = Array.from(
        document.querySelectorAll(".one-to-many-field"),
    );
    const fieldContentUrls = oneToManyFields.map(field => field.querySelector("[data-content-url]").dataset.contentUrl);
    const htmlForFieldContents = await Promise.all(fieldContentUrls.map(fieldContentUrl => getFieldContent(fieldContentUrl)));
    oneToManyFields.forEach((field, i) => {
        const fieldContentPlaceholder = field.querySelector("[data-content-url]");
        // Load in initial content.
        const fieldContent = htmlToNode(htmlForFieldContents[i].initial_content.trim());
        fieldContentPlaceholder.replaceWith(fieldContent);
        // Set up the editor for a new resource.
        fieldContent.append(htmlToNode(htmlForFieldContents[i].new_editor.trim()));
        const fkForms = document.querySelector("#fk-forms");
        fkForms.append(htmlToNode(htmlForFieldContents[i].empty_new_form.trim()));
        // Set up the editor for updates and the delete dialog.
        const dialogs = document.querySelector("#dialogs");
        const templatesForResources = htmlForFieldContents[i].existing_resource_templates;
        for (const resourceId in templatesForResources) {
            const templatesForResource = templatesForResources[resourceId];
            fkForms.append(htmlToNode(templatesForResource.empty_update_form.trim()));
            fieldContent.append(htmlToNode(templatesForResource.update_editor.trim()));
            dialogs.append(htmlToNode(templatesForResource.delete_dialog.trim()));
        }
        // Set up the templates for new items.
        const headElement = document.querySelector("head");
        const templates = htmlForFieldContents[i].templates;
        headElement.append(htmlToNode(templates.update_editor.trim()));
        headElement.append(htmlToNode(templates.empty_update_form.trim()));
        headElement.append(htmlToNode(templates.delete_dialog.trim()));
        headElement.append(htmlToNode(templates.list_item.trim()));
        new OneToManyFieldWithEditor(field);
    });
}
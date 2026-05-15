import { AsyncForeignKeyFieldFormHandler } from "/static/editor/async_forms.js";
import { FormDialog } from "/static/editor/form_dialog.js";
import { displayToast } from "/static/editor/toasts.js";
import { htmlToNode } from "/static/editor/utils.js";

class OneToOneFieldWithEditor {
    constructor(oneToOneField) {
        this.oneToOneField = oneToOneField;
        this.setupClassFields();
        this.setupEditors();
        this.setupDeleteDialog();
    }

    setupClassFields() {
        // Default content
        this.defaultContent = this.oneToOneField.querySelector(
            ".initial-content"
        );
        // New editor button
        this.newEditorButton = this.oneToOneField.querySelector(
            "button.new-editor-btn[data-editor-id]",
        );
        this.newEditorElement = document.querySelector(
            `#${this.newEditorButton.dataset.editorId}`,
        );
        this.newEditorForm = document.querySelector(
            `#${this.newEditorElement.dataset.formId}`
        );
        // Update editor button
        this.updateEditorButton = this.oneToOneField.querySelector(
            "button.update-editor-btn[data-editor-id]",
        );
        this.updateEditorElement = document.querySelector(
            `#${this.updateEditorButton.dataset.editorId}`,
        );
        this.updateEditorForm = document.querySelector(
            `#${this.updateEditorElement.dataset.formId}`
        );
        // Delete dialog button
        this.deleteDialogButton = this.oneToOneField.querySelector(
            "button.delete-dialog-btn[data-dialog-id]",
        );
        this.deleteDialogElement = document.querySelector(
            `#${this.deleteDialogButton.dataset.dialogId}`,
        );
        this.deleteDialogForm = this.deleteDialogElement.querySelector("form");
        this.resourceType = this.oneToOneField.dataset.resourceType;
    }

    setupEditors() {
        this.setupNewEditor();
        this.setupUpdateEditor();
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
                this.newEditorButton.classList.add("d-none");
                this.updateEditorButton.classList.remove("d-none");
                this.deleteDialogButton.classList.remove("d-none");
                for (const property in responseData.resource) {
                    let propertyValue = responseData.resource[property];
                    const elementForProperty =
                        this.oneToOneField.querySelector(
                            `[data-field="${property}"]`,
                        );
                    if (!elementForProperty) continue;
                    elementForProperty.textContent = propertyValue;
                    if (!propertyValue) {
                        elementForProperty.textContent = "None";
                    }
                    const fieldForProperty =
                        document.querySelector(
                            `[form="${this.updateEditorForm.id}"][name="${property}"]`,
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
                    this.updateEditorForm.reset();
                }
                this.deleteDialogForm.querySelector(
                    "[name='resource_id_to_delete']",
                ).value = responseData.resource.pk;
                displayToast(`Registered ${this.resourceType} ${responseData.resource.pk}.`);
            },
            statusButtonSelector: `button[form="${this.newEditorForm.id}"]`,
        });
        asyncFormHandler.setup();
    }

    setupUpdateEditor() {
        this.updateEditorButton.addEventListener("click", () => {
            this.defaultContent.classList.add("d-none");
            this.updateEditorElement.classList.remove("d-none");
        });
        const backButton = this.updateEditorElement.querySelector("button[data-back-id]");
        backButton.addEventListener("click", () => {
            this.defaultContent.classList.remove("d-none");
            this.updateEditorElement.classList.add("d-none");
        });
        const asyncFormHandler = new AsyncForeignKeyFieldFormHandler(this.updateEditorForm, {
            onSuccess: (responseData) => {
                for (const property in responseData.resource) {
                    let propertyValue = responseData.resource[property];
                    // Set the value preview element displaying the property's
                    // value before the editor is open.
                    const elementForProperty =
                        this.oneToOneField.querySelector(
                            `[data-field="${property}"]`,
                        );
                    if (!elementForProperty) continue;
                    elementForProperty.textContent = propertyValue;
                    if (Array.isArray(propertyValue)) {
                        elementForProperty.textContent =
                            propertyValue.join(", ");
                    }
                    if (!propertyValue) {
                        elementForProperty.textContent = "None";
                    }
                    // Set the value of multiple input fields assigned
                    // for the property (if applicable).
                    const fieldsForProperty = Array.from(
                        document.querySelectorAll(
                            `[form="${this.updateEditorForm.id}"][data-multi-value-field="${property}"]`,
                        ),
                    );
                    if (fieldsForProperty.length !== 0) {
                        if (propertyValue === null) {
                            propertyValue = "";
                            fieldsForProperty.forEach(
                                (field) =>
                                    (field.defaultValue = propertyValue),
                            );
                            continue;
                        }
                        fieldsForProperty.forEach((field, i) => {
                            field.defaultValue = propertyValue[i];
                        });
                        continue;
                    }
                    // Set the input field value for the property.
                    const fieldForProperty =
                        document.querySelector(
                            `[form="${this.updateEditorForm.id}"][name="${property}"]`,
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
                    this.newEditorButton.classList.remove("d-none");
                    this.updateEditorButton.classList.add("d-none");
                    this.deleteDialogButton.classList.add("d-none");
                    Array.from(
                        document.querySelectorAll(
                            `input[form="${this.updateEditorForm.id}"],
                            textarea[form="${this.updateEditorForm.id}"],
                            select[form="${this.updateEditorForm.id}"]`,
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
                    this.updateEditorForm.reset();
                    Array.from(
                        this.oneToOneField.querySelectorAll("[data-field]"),
                    ).forEach((element) => {
                        element.textContent = "None";
                    });
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

export async function loadOneToOneFields() {
    const oneToOneFields = Array.from(
        document.querySelectorAll(".one-to-one-field"),
    );
    const fieldContentUrls = oneToOneFields.map(field => field.querySelector("[data-content-url]").dataset.contentUrl);
    const htmlForFields = await Promise.all(fieldContentUrls.map(fieldContentUrl => getFieldContent(fieldContentUrl)));
    oneToOneFields.forEach((field, i) => {
        const fieldContentPlaceholder = field.querySelector("[data-content-url]");
        const fieldContent = htmlToNode(htmlForFields[i].initial_content.trim());
        fieldContentPlaceholder.replaceWith(fieldContent);
        fieldContent.append(htmlToNode(htmlForFields[i].new_editor.trim()));
        fieldContent.append(htmlToNode(htmlForFields[i].update_editor.trim()));
        const dialogs = document.querySelector("#dialogs");
        dialogs.append(htmlToNode(htmlForFields[i].delete_dialog.trim()));
        const fkForms = document.querySelector("#fk-forms");
        fkForms.append(htmlToNode(htmlForFields[i].empty_new_form.trim()));
        fkForms.append(htmlToNode(htmlForFields[i].empty_update_form.trim()));
        new OneToOneFieldWithEditor(field);
    });
}
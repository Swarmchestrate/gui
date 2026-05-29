import { FormDialog } from "/static/editor/form_dialog.js";
import { displayToast } from "/static/editor/toasts.js";
import { htmlToNode } from "/static/editor/utils.js";

class OneToOneField {
    constructor(oneToOneField) {
        this.oneToOneField = oneToOneField;
        this.setupClassFields();
        this.setupDeleteDialog();
    }

    setupClassFields() {
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
                    displayToast(`Deleted ${this.resourceType} ${this.deleteDialogForm.querySelector(
                        "[name='resource_id_to_delete']"
                    ).value}.`);
                },
            },
            this.deleteDialogForm,
        );
    }
}

async function getSection(sectionUrl) {
    const response = await fetch(
        sectionUrl,
        { method: "GET" },
    );
    if (!response.ok) {
        console.error(
            "Received an error whilst loading an editor section: ",
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
        "Could not load an editor section due to an error: ",
        error,
    );
}

export async function loadNonDialogBasedOneToOneFieldSections() {
    const oneToOneFieldSections = Array.from(
        document.querySelectorAll(".one-to-one-field[data-editor-based]"),
    );
    const sectionUrls = oneToOneFieldSections.map(section => section.querySelector("[data-section-url]").dataset.sectionUrl);
    const htmlForSections = await Promise.all(sectionUrls.map(sectionUrl => getSection(sectionUrl)));
    oneToOneFieldSections.forEach((section, i) => {
        const sectionPlaceholder = section.querySelector("[data-section-url]");
        sectionPlaceholder.replaceWith(htmlToNode(htmlForSections[i].section.trim()));
        const dialogsSection = document.querySelector("#dialogs");
        dialogsSection.append(htmlToNode(htmlForSections[i].delete_dialog.trim()));
        new OneToOneField(section);
    });
}

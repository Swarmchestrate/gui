import { FormDialog } from "/static/editor/form_dialog.js";
import { displayToast } from "/static/editor/toasts.js";
import { htmlToNode } from "/static/editor/utils.js";

class OneToManyField {
    constructor(oneToManyField) {
        this.oneToManyField = oneToManyField;
        this.list = oneToManyField.querySelector("ul.list-group");
        this.fieldName = oneToManyField.dataset.field;
        this.setupClassFields();
        this.setupExistingListItems();
    }

    setupClassFields() {
        // HTML template strings
        this.resourceType = this.oneToManyField.dataset.resourceType;
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
        new OneToManyFieldListItem(listItem, this.resourceType, {
            onDelete: () => {
                if (Array.from(this.list.children).length === 0) {
                    this.list.replaceChildren();
                }
            }
        });
    }
}

class OneToManyFieldListItem {
    constructor(listItem, resourceType, options) {
        if (!("onDelete" in options)) {
            options.onDelete = () => {};
        }
        this.options = options;
        this.listItem = listItem;
        this.resourceType = resourceType;
        this.setupClassFields();
        this.setupDeleteDialog();
    }

    setupClassFields() {
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
                    this.options.onDelete();
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

export async function loadOneToManyFieldSections() {
    const oneToManyFieldSections = Array.from(
        document.querySelectorAll(".one-to-many-field:not([data-popup-based])"),
    );
    const sectionUrls = oneToManyFieldSections.map(section => section.querySelector("[data-section-url]").dataset.sectionUrl);
    const responses = await Promise.all(sectionUrls.map(sectionUrl => getSection(sectionUrl)));
    const dialogsContainer = document.querySelector("#dialogs");
    oneToManyFieldSections.forEach((section, i) => {
        const addButtonPlaceholder = section.querySelector(".add-fk-btn");
        addButtonPlaceholder.href = responses[i].add_url;
        addButtonPlaceholder.removeAttribute("aria-disabled");
        addButtonPlaceholder.querySelector(".invisible").classList.remove("invisible");
        addButtonPlaceholder.classList.remove(
            "disabled",
            "placeholder",
            "placeholder-wave",
            "bg-secondary-subtle"
        );
        const sectionPlaceholder = section.querySelector("[data-section-url]");
        sectionPlaceholder.replaceWith(htmlToNode(responses[i].section.trim()));
        const dialogsForResources = responses[i].resource_dialogs;
        for (const resourceId in dialogsForResources) {
            const dialogsForResource = dialogsForResources[resourceId];
            dialogsContainer.append(htmlToNode(dialogsForResource.delete_dialog.trim()));
        }
        new OneToManyField(section);
    });
}

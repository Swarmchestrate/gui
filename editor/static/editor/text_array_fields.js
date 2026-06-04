import { htmlToNode } from "/static/editor/utils.js";

class TextArrayField {
    constructor(field) {
        this.field = field;
        this.jsonOutputElement = field.querySelector("input[type='hidden']");
        this.setupClassFields();
        this.setupAddListItemButton();
        this.setupExistingListItems();
    }

    setupClassFields() {
        this.fieldId = this.field.dataset.fieldId;
        this.fieldName = this.field.dataset.fieldName;
        this.fieldLabel = this.field.dataset.fieldLabel;
        this.list = this.field.querySelector("ul.list-group");
        this.addListItemButton = this.field.querySelector(".add-btn");
        this.listItemTemplate = JSON.parse(document.querySelector("#text-array-field-list-item-template").textContent.trim());
    }

    setupAddListItemButton() {
        this.addListItemButton.addEventListener("click", () => {
            const numListItems = Array.from(this.list.children).length;
            const listItemTemplateStringFormatted = this.listItemTemplate
            .trim()
            .replaceAll("__field_id__", this.fieldId)
            .replaceAll("__field_label__", this.fieldLabel)
            .replaceAll("__counter__", numListItems);
            const newListItem = htmlToNode(listItemTemplateStringFormatted);
            this.list.append(newListItem);
            this.setupListItem(newListItem);
        });
    }

    setupExistingListItems() {
        const existingListItems = Array.from(this.field.querySelectorAll("li"));
        for (const listItem of existingListItems) {
            this.setupListItem(listItem);
        }
    }

    exportData() {
        const textInputs = Array.from(this.list.querySelectorAll("input[type='text']"));
        const data = textInputs.map(textInput => textInput.value);
        this.jsonOutputElement.value = JSON.stringify(data);
    }

    setupListItem(listItem) {
        const textInput = listItem.querySelector("input[type='text']");
        textInput.addEventListener("input", () => {
            this.exportData();
        });
        const deleteButton = listItem.querySelector(".delete-btn");
        deleteButton.addEventListener("click", () => {
            listItem.remove();
        });
    }
}

export function setupTextArrayFields() {
    const textArrayFields = document.querySelectorAll(".text-array-field");
    for (const field of textArrayFields) {
        new TextArrayField(field);
    }
}

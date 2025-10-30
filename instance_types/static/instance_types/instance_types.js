import { setupDialog } from "/static/dialog.js";
import { EditorForm } from "/static/editor/editor.js";
import {
    htmlToNode,
    updateElementPlaceholderAttributes,
} from "/static/editor/utils.js";

class InstanceTypesList {
    constructor(listId, listItemTemplateId, totalFormsetsInput) {
        this.listElement = document.querySelector(`#${listId}`);
        this.listItemTemplateHtml = JSON.parse(
            document.querySelector(`#${listItemTemplateId}`).textContent,
        ).trim();
        this.totalFormsetsInput = totalFormsetsInput;
        this.addNewButton = this.listElement.querySelector(
            "#add-instance-type-button",
        );
        this.setupAddNewButton();
        Array.from(this.listElement.children).forEach((listItem, i) => {
            this.linkListItemToDialog(listItem);
        });
        const deleteCheckboxes = document.querySelectorAll(".delete-list-item");
        const tooltipList = [...deleteCheckboxes].map(
            (checkbox) => new bootstrap.Tooltip(checkbox),
        );
    }

    getListItem(listItemIndex) {
        return this.listElement.querySelector(
            `li:nth-of-type(${listItemIndex + 1})`,
        );
    }

    getListItemIndex(listItem) {
        return Array.from(this.listElement.children).indexOf(listItem);
    }

    createListItem() {
        return htmlToNode(this.listItemTemplateHtml);
    }

    appendListItem(listItem) {
        this.listElement.insertBefore(listItem, this.addNewButton);
    }

    createAndAppendNewListItem(initialData, formsetInstanceIndex) {
        const newListItem = this.createListItem();
        updateElementPlaceholderAttributes(newListItem, formsetInstanceIndex);
        this.appendListItem(newListItem);
        this.updateListItem(newListItem, initialData);
        return newListItem;
    }

    updateListItemByIndex(listItemIndex, updateData) {
        const listItem = this.getListItem(listItemIndex);
        this.updateListItem(listItem);
    }

    updateListItem(listItem, updateData) {
        // Set name
        listItem.querySelector(".name").textContent = updateData.name;
        // Set num CPUs
        listItem.querySelector(".num-cpus").textContent = updateData.numCpus;
        // Set memory size
        listItem.querySelector(".num-memory-size").textContent =
            updateData.memorySize;
        // Set disk size
        listItem.querySelector(".num-disk-size").textContent =
            updateData.diskSize;
        // Set energy consumption
        listItem.querySelector(".num-energy-consumption").textContent =
            updateData.energyConsumption;
        // Set bandwidth
        listItem.querySelector(".num-bandwidth").textContent =
            updateData.bandwidth;
        // Set price
        listItem.querySelector(".num-price").textContent = updateData.price;
        if (updateData.unsaved) {
            listItem.classList.add("list-group-item-light");
        }
    }

    setupAddNewButton() {
        const dialog = new NewInstanceTypeDialog(
            "instance-type-__prefix__-dialog",
        );
        dialog.addShowButton(this.addNewButton);
        dialog.dialogElement.addEventListener("close", async () => {
            const dialogReturnValue = dialog.dialogElement.returnValue;
            if (!dialogReturnValue) {
                return;
            }
            const initialInstanceTypeData = JSON.parse(dialogReturnValue);
            const formsetInstanceIndex = this.listElement.children.length - 1;
            const dialogForNewInstanceType =
                createInstanceTypeFormsetInstanceDialog(
                    dialog.dialogElement.id,
                    formsetInstanceIndex,
                );
            const newListItem = this.createAndAppendNewListItem(
                initialInstanceTypeData,
                formsetInstanceIndex,
            );
            dialogForNewInstanceType.addShowButton(
                newListItem.querySelector("a"),
            );
            this.setupListItem(newListItem, dialogForNewInstanceType);
            this.totalFormsetsInput.value = this.listElement.querySelectorAll(
                "li.list-group-item-action",
            ).length;
        });
    }

    setupListItem(listItem, dialog) {
        const dialogFormInputValues = dialog.getFormInputValues();
        this.updateListItem(listItem, dialogFormInputValues);
        dialog.dialogElement.addEventListener("close", async () => {
            const dialogReturnValue = dialog.dialogElement.returnValue;
            if (!dialogReturnValue) {
                return;
            }
            const updatedInstanceTypeData = JSON.parse(dialogReturnValue);
            this.updateListItem(listItem, updatedInstanceTypeData);
        });
    }

    linkListItemToDialog(listItem) {
        if (!listItem.dataset.dialogId) return;
        const dialog = new InstanceTypeDialog(
            listItem.dataset.dialogId,
            this.getListItemIndex(listItem),
        );
        dialog.addShowButton(listItem.querySelector("a.stretched-link"), {
            lightDismiss: false,
        });
        this.setupListItem(listItem, dialog);
    }
}

class InstanceTypeDialog {
    constructor(dialogId, formsetInstanceIndex) {
        if (typeof formsetInstanceIndex === "undefined") {
            formsetInstanceIndex = "__prefix__";
        }
        this.formsetInstanceIndex = formsetInstanceIndex;
        this.dialogElement = document.querySelector(`#${dialogId}`);
        this.inputs = Array.from(this.dialogElement.querySelectorAll("input"));
        this.closeButton = this.dialogElement.querySelector(".btn-close");
        this.cancelButton = this.dialogElement.querySelector(".cancel-btn");
        this.confirmButton = this.dialogElement.querySelector(".confirm-btn");
        this.setupConfirmButton();
    }

    getFormInputValues = () => {
        return {
            name: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-name']`,
            ).value,
            numCpus: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-num_cpus']`,
            ).value,
            memorySize: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-mem_size']`,
            ).value,
            diskSize: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-disk_size']`,
            ).value,
            energyConsumption: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-energy_consumption']`,
            ).value,
            bandwidth: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-bandwidth']`,
            ).value,
            price: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-price']`,
            ).value,
            unsaved: this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-unsaved']`,
            ).value,
        };
    };

    setupConfirmButton() {
        this.confirmButton.addEventListener("click", () => {
            this.dialogElement.querySelector(
                `input[name='instance_types-${this.formsetInstanceIndex}-unsaved']`,
            ).value = true;
            const returnValue = this.getFormInputValues();
            this.dialogElement.close(JSON.stringify(returnValue));
        });
    }

    addShowButton(showButton, options) {
        setupDialog(
            this.dialogElement,
            [this.closeButton, this.cancelButton],
            [showButton],
            options,
        );
    }
}

class NewInstanceTypeDialog extends InstanceTypeDialog {
    resetInputs() {
        this.inputs.forEach((input) => {
            input.value = "";
        });
    }
}

const createInstanceTypeFormsetInstanceDialog = (
    dialogTemplateId,
    formsetInstanceIndex,
) => {
    const dialogTemplateClone = document
        .querySelector(`#${dialogTemplateId}`)
        .cloneNode(true);
    dialogTemplateClone.setAttribute(
        "id",
        dialogTemplateClone.id.replace("__prefix__", formsetInstanceIndex),
    );
    updateElementPlaceholderAttributes(
        dialogTemplateClone,
        formsetInstanceIndex,
    );
    const instanceTypesSection = document.querySelector(
        "#instance-types-section",
    );
    instanceTypesSection.appendChild(dialogTemplateClone);
    return new InstanceTypeDialog(dialogTemplateClone.id, formsetInstanceIndex);
};

window.addEventListener("DOMContentLoaded", () => {
    const instanceTypesList = new InstanceTypesList(
        "instance-types-list",
        "instance-type-list-item-template",
        document.querySelector("#id_instance_types-TOTAL_FORMS"),
    );
});

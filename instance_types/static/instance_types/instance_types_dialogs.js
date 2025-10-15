import { addShowButtonToDialog, setupDialog } from "/static/dialog.js";

const instanceTypesList = document.querySelector("#instance-types-list");
const instanceTypesTotalNumberInput = document.querySelector(
    "#id_instance_types-TOTAL_FORMS",
);
const instanceTypeFormsetsWrapper = document.querySelector(
    "#instance-types-formset-wrapper",
);
const instanceTypeDialog = document.querySelector("#instance-type-dialog");
const instanceTypeListItemTemplate = JSON.parse(
    document.querySelector("#instance-type-list-item-template").textContent,
);
const addInstanceTypeButton = document.querySelector(
    "#add-instance-type-button",
);
const instanceTypeDialogCloseButton =
    instanceTypeDialog.querySelector(".btn-close");

const instanceTypeNameInputName = "instance_types-__prefix__-name";
const instanceTypeNumCpusInputName = "instance_types-__prefix__-num_cpus";
const instanceTypeMemorySizeInputName = "instance_types-__prefix__-mem_size";
const instanceTypeDiskSizeInputName = "instance_types-__prefix__-disk_size";
const instanceTypeEnergyConsumptionInputName =
    "instance_types-__prefix__-energy_consumption";
const instanceTypeBandwidthInputName = "instance_types-__prefix__-bandwidth";
const instanceTypePriceInputName = "instance_types-__prefix__-price";
let instanceTypeToUpdateNumber;

function htmlToNode(html) {
    // Credit: https://stackoverflow.com/a/35385518/10640126
    const template = document.createElement("TEMPLATE");
    template.innerHTML = html;
    const numNodes = template.content.childNodes.length;
    if (numNodes !== 1) {
        throw new Error(`html parameter must represent a single node; got ${numNodes} nodes.
            Note that leading or trailing spaces around an element in your HTML, like
            "</img> ", get parsed as text nodes neighbouring the element; call .trim() on
            your input to avoid this.
        `);
    }
    return template.content.firstChild;
}

function setInstanceTypeListItemValues(
    instanceTypeMetadata,
    instanceTypeListItem,
) {
    // Set name
    instanceTypeListItem.querySelector(".name").textContent =
        instanceTypeMetadata[instanceTypeNameInputName];
    // Set num CPUs
    instanceTypeListItem.querySelector(".num-cpus").textContent =
        instanceTypeMetadata[instanceTypeNumCpusInputName];
    // Set memory size
    instanceTypeListItem.querySelector(".num-memory-size").textContent =
        instanceTypeMetadata[instanceTypeMemorySizeInputName];
    // Set disk size
    instanceTypeListItem.querySelector(".num-disk-size").textContent =
        instanceTypeMetadata[instanceTypeDiskSizeInputName];
    // Set energy consumption
    instanceTypeListItem.querySelector(".num-energy-consumption").textContent =
        instanceTypeMetadata[instanceTypeEnergyConsumptionInputName];
    // Set bandwidth
    instanceTypeListItem.querySelector(".num-bandwidth").textContent =
        instanceTypeMetadata[instanceTypeBandwidthInputName];
    // Set price
    instanceTypeListItem.querySelector(".num-price").textContent =
        instanceTypeMetadata[instanceTypePriceInputName];
}

function setDialogFormInputValues(instanceTypeMetadata) {
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeNameInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypeNameInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeNumCpusInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypeNumCpusInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeMemorySizeInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypeMemorySizeInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeDiskSizeInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypeDiskSizeInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeEnergyConsumptionInputName}"]`,
    ).value =
        instanceTypeMetadata[instanceTypeEnergyConsumptionInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypeBandwidthInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypeBandwidthInputName] || "";
    instanceTypeDialog.querySelector(
        `input[name="${instanceTypePriceInputName}"]`,
    ).value = instanceTypeMetadata[instanceTypePriceInputName] || "";
}

function replacePlaceholdersInFormsetInputAttributes(
    instanceTypeFormsetClone,
    formsetNumber,
) {
    const formsetTemplateElements = instanceTypeFormsetClone.querySelectorAll(
        '[id*="__prefix__"], [for*="__prefix__"], [name*="__prefix__"]',
    );
    for (const element of formsetTemplateElements) {
        for (const attribute of element.attributes) {
            if (!attribute.value.includes("__prefix__")) {
                continue;
            }
            element.setAttribute(
                attribute.name,
                attribute.value.replace("__prefix__", formsetNumber),
            );
        }
    }
    return instanceTypeFormsetClone;
}

function setupInstanceTypeListItemOnClick(
    instanceTypeMetadata,
    instanceTypeListItem,
) {
    instanceTypeListItem.addEventListener("click", () => {
        setDialogFormInputValues(instanceTypeMetadata);
    });
    addShowButtonToDialog(
        instanceTypeListItem,
        instanceTypeDialog,
        instanceTypeDialogCloseButton,
    );
}

function setupInstanceTypeDialog() {
    if (!addInstanceTypeButton) {
        return;
    }
    addInstanceTypeButton.addEventListener("click", () => {
        instanceTypeToUpdateNumber = undefined;
        setDialogFormInputValues({});
    });
    setupDialog(
        instanceTypeDialog,
        instanceTypeDialogCloseButton,
        [addInstanceTypeButton],
        {
            closeOnBackdropClick: false,
        },
    );
    for (const instanceTypeListItem of instanceTypesList.children) {
        if (instanceTypeListItem === addInstanceTypeButton) {
            continue;
        }
        const listItemIndex = Array.from(instanceTypesList.children).indexOf(
            instanceTypeListItem,
        );
        const correspondingFormsetInputs =
            instanceTypeFormsetsWrapper.querySelectorAll(
                `.instance-type-form:nth-of-type(${listItemIndex + 1}) input`,
            );
        const instanceTypeMetadata = {};
        for (const input of correspondingFormsetInputs) {
            const metadataKey = input.name.replace(listItemIndex, "__prefix__");
            instanceTypeMetadata[metadataKey] = input.value;
        }
        setupInstanceTypeListItemOnClick(
            instanceTypeMetadata,
            instanceTypeListItem,
        );
    }
    const dialogConfirmButton =
        instanceTypeDialog.querySelector(".confirm-btn");
    dialogConfirmButton.addEventListener("click", (e) => {
        e.preventDefault();
        const form = instanceTypeDialog.querySelector("form");
        const formData = new FormData(form);
        instanceTypeDialog.close(JSON.stringify(Object.fromEntries(formData)));
    });
    instanceTypeDialog.addEventListener("close", (e) => {
        const returnValue = instanceTypeDialog.returnValue;
        if (returnValue === "cancel" || returnValue === "") {
            return;
        }
        const instanceTypeMetadata = JSON.parse(returnValue);
        const instanceTypeFormsetClone = instanceTypeDialog
            .querySelector(".instance-type-form")
            .cloneNode(true);
        if (instanceTypeToUpdateNumber !== undefined) {
            // Update the values of an existing formset
            const listItemToUpdate = instanceTypesList.querySelector(
                `button:nth-child(${instanceTypeToUpdateNumber + 1})`,
            );
            const updatedInstanceTypeFormsetClone =
                replacePlaceholdersInFormsetInputAttributes(
                    instanceTypeFormsetClone,
                    instanceTypeToUpdateNumber,
                );
            // Replace corresponding formset with updated values.
            instanceTypeFormsetsWrapper
                .querySelector(
                    `.instance-type-form:nth-of-type(${instanceTypeToUpdateNumber + 1})`,
                )
                .replaceWith(updatedInstanceTypeFormsetClone);
            return setInstanceTypeListItemValues(
                instanceTypeMetadata,
                listItemToUpdate,
            );
        }
        const newInstanceTypeListItem = htmlToNode(
            instanceTypeListItemTemplate.trim(),
        );
        setInstanceTypeListItemValues(
            instanceTypeMetadata,
            newInstanceTypeListItem,
        );
        instanceTypesList.insertBefore(
            newInstanceTypeListItem,
            addInstanceTypeButton,
        );
        const updatedInstanceTypeFormsetClone =
            replacePlaceholdersInFormsetInputAttributes(
                instanceTypeFormsetClone,
                instanceTypeFormsetsWrapper.querySelectorAll(
                    ".instance-type-form",
                ).length,
            );
        instanceTypeFormsetsWrapper.appendChild(
            updatedInstanceTypeFormsetClone,
        );
        instanceTypesTotalNumberInput.value =
            instanceTypeFormsetsWrapper.querySelectorAll(
                ".instance-type-form",
            ).length;
        setupInstanceTypeListItemOnClick(
            instanceTypeMetadata,
            newInstanceTypeListItem,
        );
    });
}

window.addEventListener("DOMContentLoaded", () => {
    setupInstanceTypeDialog();
});

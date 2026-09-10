import { setupDialog } from "/static/dialog.js";

function swapListItemNumbersAndResortList(listItem1, listItem2, sortable) {
    const listItem1Number = listItem1.dataset.id;
    const listItem2Number = listItem2.dataset.id;
    listItem1.setAttribute("data-id", listItem2Number);
    listItem2.setAttribute("data-id", listItem1Number);
    const order = sortable.toArray().map(num => parseInt(num)).sort((a, b) => {
        return a - b;
    });
    sortable.sort(order, true);
}

export function setupCategoryOrderDialog() {
    function updateCategoryOrderInForm(form, listItems) {
        const categoryOrderInput = form.querySelector("input[name='category_order']");
        const orderData = listItems.map(listItem => listItem.dataset.categoryName);
        categoryOrderInput.value = JSON.stringify(orderData);
    }

    const dialogButton = document.querySelector(".category-order-btn");
    if (!dialogButton) return;
    const dialogId = dialogButton.dataset.dialogId;
    const dialog = document.querySelector(`#${dialogId}`);
    if (!dialog) {
        return console.error(`Category order dialog #${dialogId} not found.`);
    }
    setupDialog(
        dialog,
        [
            dialog.querySelector(".btn-close"),
        ],
        [dialogButton],
    );
    const categoryList = dialog.querySelector("ul");
    if (!categoryList) return;
    const form = dialog.querySelector("form");
    if (!form) return;
    const sortable = new Sortable(categoryList, {
        handle: ".handle",
        animation: 150,
        onMove: () => {
            window.setTimeout(() => {
                const listItems = Array.from(categoryList.querySelectorAll("li"));
                listItems.forEach((listItem, i) => {
                    listItem.setAttribute("data-id", (i + 1));
                });
                updateCategoryOrderInForm(form, listItems);
            }, 0.25);
        },
    });
    const categoryListItems = Array.from(categoryList.querySelectorAll("li"));
    categoryListItems.forEach(listItem => {
        const moveUpButton = listItem.querySelector(".move-up-button");
        moveUpButton.addEventListener("click", () => {
            const previousListItem = listItem.previousElementSibling;
            if (!previousListItem) return;
            swapListItemNumbersAndResortList(
                listItem,
                previousListItem,
                sortable
            );
            updateCategoryOrderInForm(form, categoryListItems);
        });
        const moveDownButton = listItem.querySelector(".move-down-button");
        moveDownButton.addEventListener("click", () => {
            const nextListItem = listItem.nextElementSibling;
            if (!nextListItem) return;
            swapListItemNumbersAndResortList(
                listItem,
                nextListItem,
                sortable
            );
            updateCategoryOrderInForm(form, categoryListItems);
        });
    });
}

export function setupFieldOrderDialog() {
    function updateFieldOrderInForm(form, fieldOrderLists) {
        const fieldOrderInput = form.querySelector("input[name='field_order']");
        const orderData = {};
        fieldOrderLists.forEach(orderList => {
            const categoryName = orderList.dataset.categoryName;
            const listItems = Array.from(orderList.querySelectorAll("li"));
            orderData[categoryName] = listItems.map(listItem => listItem.dataset.fieldPk);
        });
        fieldOrderInput.value = JSON.stringify(orderData);
    }

    const dialogButton = document.querySelector(".field-order-btn");
    if (!dialogButton) return;
    const dialogId = dialogButton.dataset.dialogId;
    const dialog = document.querySelector(`#${dialogId}`);
    if (!dialog) {
        return console.error(`Field order dialog #${dialogId} not found.`);
    }
    setupDialog(
        dialog,
        [
            dialog.querySelector(".btn-close"),
        ],
        [dialogButton],
    );
    const fieldOrderLists = Array.from(dialog.querySelectorAll("ul"));
    if (!fieldOrderLists) return;
    const form = dialog.querySelector("form");
    if (!form) return;
    fieldOrderLists.forEach(fieldOrderList => {
        const sortable = new Sortable(fieldOrderList, {
            handle: ".handle",
            animation: 150,
            onMove: () => {
                window.setTimeout(() => {
                    const listItems = Array.from(fieldOrderList.querySelectorAll("li"));
                    listItems.forEach((listItem, i) => {
                        listItem.setAttribute("data-id", (i + 1));
                    });
                    updateFieldOrderInForm(form, fieldOrderLists);
                }, 0.25);
            },
        });
        const fieldOrderListItems = Array.from(fieldOrderList.querySelectorAll("li"));
        fieldOrderListItems.forEach(listItem => {
            const moveUpButton = listItem.querySelector(".move-up-button");
            moveUpButton.addEventListener("click", () => {
                const previousListItem = listItem.previousElementSibling;
                if (!previousListItem) return;
                swapListItemNumbersAndResortList(
                    listItem,
                    previousListItem,
                    sortable
                );
                updateFieldOrderInForm(form, fieldOrderLists);
            });
            const moveDownButton = listItem.querySelector(".move-down-button");
            moveDownButton.addEventListener("click", () => {
                const nextListItem = listItem.nextElementSibling;
                if (!nextListItem) return;
                swapListItemNumbersAndResortList(
                    listItem,
                    nextListItem,
                    sortable
                );
                updateFieldOrderInForm(form, fieldOrderLists);
            });
        });
    });
}
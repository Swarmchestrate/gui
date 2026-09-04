export function updateCategoryOrderInForm(form, listItems) {
    const categoryOrderInput = form.querySelector("input[name='category_order']");
    const categoriesOrdered = listItems.map(listItem => listItem.dataset.categoryName);
    categoryOrderInput.value = JSON.stringify(categoriesOrdered);
}

export function swapListItemNumbersAndResortList(listItem1, listItem2, sortable) {
    const listItem1Number = listItem1.dataset.id;
    const listItem2Number = listItem2.dataset.id;
    listItem1.setAttribute("data-id", listItem2Number);
    listItem2.setAttribute("data-id", listItem1Number);
    const order = sortable.toArray().map(num => parseInt(num)).sort((a, b) => {
        return a - b;
    });
    sortable.sort(order, true);
}
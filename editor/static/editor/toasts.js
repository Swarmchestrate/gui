import { htmlToNode } from "/static/editor/utils.js";

const toastContainer = document.querySelector("#toast-container");
const toastTemplateHtml = JSON.parse(
    document.querySelector("#toast-template").textContent,
).trim();

function createNewToastElement() {
    return htmlToNode(toastTemplateHtml);
}

function appendToastToContainer(toastElement) {
    toastContainer.appendChild(toastElement);
}

export function displayToast(title, message) {
    const newToastElement = createNewToastElement();
    newToastElement.querySelector(".toast-header strong").textContent = title;
    newToastElement.querySelector(".toast-body").textContent = message;
    appendToastToContainer(newToastElement);
    const bootstrapToast = new bootstrap.Toast(newToastElement, {});
    bootstrapToast.show();
}

export function displayToastWithoutAutoHide(title, message) {
    const newToastElement = createNewToastElement();
    newToastElement.querySelector(".toast-header strong").textContent = title;
    newToastElement.querySelector(".toast-body").textContent = message;
    appendToastToContainer(newToastElement);
    const bootstrapToast = new bootstrap.Toast(newToastElement, {
        autohide: false,
    });
    bootstrapToast.show();
}

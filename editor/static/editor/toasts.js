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

export function displayToast(message) {
    const newToastElement = createNewToastElement();
    newToastElement.querySelector(".toast-body").textContent = message;
    appendToastToContainer(newToastElement);
    const bootstrapToast = new bootstrap.Toast(newToastElement, {});
    bootstrapToast.show();
}

export function displayToastUntilDismissed(message) {
    const newToastElement = createNewToastElement();
    newToastElement.querySelector(".toast-body").textContent = message;
    appendToastToContainer(newToastElement);
    const bootstrapToast = new bootstrap.Toast(newToastElement, {
        autohide: false,
    });
    bootstrapToast.show();
}

import { setupFormsetTables } from "/static/editor_formsets.js";

const form = document.querySelector("#editor-form");
const formSubmitButton = form.querySelector("button[type='submit']");
const loadingText = formSubmitButton.querySelector(".loading-text");
const defaultText = formSubmitButton.querySelector(".default-text");
const statusText = formSubmitButton.querySelector(".status-text");
const fields = document.querySelectorAll("input, textarea, select");
const formMessagesList = document.querySelector("#form-messages-list");

function displayFormMessages(messages) {
    clearFormMessagesList();
    messages.forEach((message) => {
        const listItem = document.createElement("li");
        listItem.textContent = message;
        formMessagesList.appendChild(listItem);
    });
    formMessagesList.classList.remove("d-none");
}

function displayFormErrors(errors) {
    formMessagesList.classList.remove("text-success");
    formMessagesList.classList.add("text-danger");
    displayFormMessages(errors);
}

function displayFormSuccessMessages(messages) {
    formMessagesList.classList.add("text-success");
    formMessagesList.classList.remove("text-danger");
    displayFormMessages(messages);
}

function displayValidationMessagesForField(
    fieldName,
    messages,
    scrollIntoView,
) {
    if (fieldName === "__all__") return;
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (!field) {
        return;
    }
    const fieldLabel = document.querySelector(`label[for="${field.id}"]`);
    const feedback = document.querySelector(`#${field.id} ~ .invalid-feedback`);
    // Scroll to first field with feedback
    if (scrollIntoView) {
        try {
            fieldLabel.scrollIntoView();
        } catch (error) {
            console.error(error);
            field.scrollIntoView();
        }
    }
    const feedbackList = document.createElement("ul");
    feedbackList.classList.add("mb-0", "p-0", "list-unstyled");
    for (const messageData of messages) {
        const errorItem = document.createElement("li");
        errorItem.textContent = messageData.message;
        feedbackList.appendChild(errorItem);
    }
    feedback.appendChild(feedbackList);
    field.classList.add("is-invalid");
}

function displayValidationMessages(validationMessages) {
    /**
     * Displays validation messages that apply to
     * specific fields and/or the whole form.
     */
    // __all__ signifies validation feedback that applies
    // to the whole form.
    const firstInvalidFieldName = Object.keys(validationMessages).find(
        (key) => key !== "__all__",
    );
    for (const fieldName in validationMessages) {
        displayValidationMessagesForField(
            fieldName,
            validationMessages[fieldName],
            fieldName === firstInvalidFieldName,
        );
    }
    if (!("__all__" in validationMessages)) {
        return;
    }
    // Display validation feedback that applies to the whole
    // form.
    displayFormErrors(
        validationMessages.__all__.map((messageData) => messageData.message),
    );
}

function clearFormMessagesList() {
    formMessagesList.replaceChildren();
}

function clearValidationMessages() {
    clearFormMessagesList();
    const allNotEmptyInvalidFeedbackElements = document.querySelectorAll(
        ".invalid-feedback:not(:empty)",
    );
    allNotEmptyInvalidFeedbackElements.forEach((element) => {
        element.replaceChildren();
    });
}

function resetInvalidFields() {
    const invalidFields = document.querySelectorAll(".is-invalid");
    invalidFields.forEach((field) => {
        field.classList.remove("is-invalid");
    });
}

function showLoadingText() {
    formSubmitButton.disabled = true;
    loadingText.classList.remove("d-none");
    defaultText.classList.add("d-none");
}

function hideLoadingText() {
    formSubmitButton.disabled = false;
    loadingText.classList.add("d-none");
    defaultText.classList.remove("d-none");
}

function updateStatusText(updatedText) {
    statusText.textContent = updatedText;
}

// Field validation
function validateField(event) {
    /**
     * Checks validity of a field and displays the
     * validation message, if any.
     */
    const field = event.currentTarget;
    const isValid = field.checkValidity();
    const feedback = document.querySelector(`#${field.id} ~ .invalid-feedback`);
    if (!isValid) {
        field.classList.add("is-invalid");
        return (feedback.textContent = field.validationMessage);
    }
    return field.classList.remove("is-invalid");
}

async function submitFormAsynchronously() {
    const data = new URLSearchParams();
    for (const pair of new FormData(form)) {
        data.append(pair[0], pair[1]);
    }
    // Request headers
    const headers = new Headers();
    headers.append("Accept", "application/json");
    const response = await fetch(form.action, {
        method: "POST",
        headers: headers,
        body: data,
    });
    let responseData;
    try {
        responseData = await response.json();
    } catch (error) {
        hideLoadingText();
        return displayFormErrors([
            "Encountered checking server validation results. Please try again.",
        ]);
    }
    if (response.ok) {
        updateStatusText(`Redirecting`);
        return (window.location.href = responseData.redirect);
    }
    hideLoadingText();
    const validationMessages = responseData.feedback || {};
    displayValidationMessages(validationMessages);
}

form.addEventListener("submit", async (event) => {
    showLoadingText();
    resetInvalidFields();
    clearValidationMessages();
    return false;
});

window.addEventListener("DOMContentLoaded", () => {
    fields.forEach((field) => {
        field.addEventListener("input", validateField);
    });
    setupFormsetTables();
});

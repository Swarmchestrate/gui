const form = document.querySelector("#editor-form");
const formSubmitButton = form.querySelector("button[type='submit']");
const loadingText = formSubmitButton.querySelector(".loading-text");
const defaultText = formSubmitButton.querySelector(".loading-text + span:not(.loading-text)");
const fields = document.querySelectorAll("input, textarea, select");


function displayValidationMessages(validationMessages) {
    /**
     * Displays validation messages that apply to
     * specific fields and/or the whole form.
     */
    // __all__ signifies validation feedback that applies
    // to the whole form.
    for (const fieldName in validationMessages) {
        if (fieldName === "__all__") continue;
        const field = document.querySelector(`[name="${fieldName}"]`);
        const feedback = document.querySelector(`#${field.id} ~ .invalid-feedback`);
        const feedbackList = document.createElement("ul");
        feedbackList.classList.add("mb-0", "p-0", "list-unstyled");
        const fieldValidationMessages = validationMessages[fieldName];
        for (const validationMessageData of fieldValidationMessages) {
            const errorItem = document.createElement("li");
            errorItem.textContent = validationMessageData.message;
            feedbackList.appendChild(errorItem);
        }
        feedback.appendChild(feedbackList);
        field.classList.add("is-invalid");
    }
    if (!"__all__" in validationMessages) {
        return;
    }
    // Display validation feedback that applies to the whole
    // form.
    const allErrorsList = document.querySelector("#all-errors-list");
    for (const error of validationMessages.__all__) {
        const errorItem = document.createElement("li");
        errorItem.textContent = error.message;
        allErrorsList.appendChild(errorItem);
    }
    allErrorsList.classList.remove("d-none");
}

function clearValidationMessages() {
    const allErrorsList = document.querySelector("#all-errors-list");
    allErrorsList.replaceChildren();
    const allNotEmptyInvalidFeedbackElements = document.querySelectorAll(".invalid-feedback:not(:empty)");
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
        return feedback.textContent = field.validationMessage;
    }
    return field.classList.remove("is-invalid");
};

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    showLoadingText();
    resetInvalidFields();
    clearValidationMessages();
    const data = new URLSearchParams();
    for (const pair of new FormData(form)) {
        data.append(pair[0], pair[1]);
    }
    const response = await fetch(`${form.action}?response_format=json`, {
        method: "POST",
        body: data,
    });
    if (response.ok) {
        return window.location.href = form.action;
    }
    hideLoadingText();
    const responseData = await response.json();
    const validationMessages = responseData.feedback || {};
    displayValidationMessages(validationMessages);
});

window.addEventListener("DOMContentLoaded", () => {
    fields.forEach((field) => {
        field.addEventListener("input", validateField);
    });
});
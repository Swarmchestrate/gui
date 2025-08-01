const form = document.querySelector("#editor-form");
const fields = document.querySelectorAll("input, textarea, select");


const validateField = (event) => {
    const field = event.currentTarget;
    const isValid = field.checkValidity();
    const feedback = document.querySelector(`#${field.id} ~ .invalid-feedback`);
    if (!isValid) {
        field.classList.add("is-invalid");
        return feedback.textContent = field.validationMessage;
    }
    return field.classList.remove("is-invalid");
};

function displayValidationMessages(validationMessages) {
    if ("__all__" in validationMessages) {
        const allErrorsList = document.querySelector("#all-errors-list");
        for (const error of validationMessages.__all__) {
            const errorItem = document.createElement("li");
            errorItem.textContent = error.message;
            allErrorsList.appendChild(errorItem);
        }
        allErrorsList.classList.remove("d-none");
    }
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
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new URLSearchParams();
    for (const pair of new FormData(form)) {
        data.append(pair[0], pair[1]);
    }
    const response = await fetch(form.action, {
        method: "POST",
        body: data,
    });
    if (response.ok) {
        return window.location.href = response.url;
    }
    const responseData = await response.json();
    const validationMessages = responseData.feedback || {};
    displayValidationMessages(validationMessages);
});

window.addEventListener("DOMContentLoaded", () => {
    fields.forEach((field) => {
        field.addEventListener("input", validateField);
    });
});
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

window.addEventListener("DOMContentLoaded", () => {
    fields.forEach((field) => {
        field.addEventListener("input", validateField);
    });
});
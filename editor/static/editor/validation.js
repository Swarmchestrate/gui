export class EditorValidator {
    constructor(form) {
        this.form = form;
        this.fields = form.querySelectorAll("input, select, textarea");
        this.formMessagesList = form.querySelector(".form-messages-list");
    }

    setupInlineValidation() {
        this.fields.forEach((field) => {
            field.addEventListener("input", this.validateField);
        });
    }

    validateField(event) {
        /**
         * Checks validity of a field and displays the
         * validation message, if any.
         */
        const field = event.currentTarget;
        const isValid = field.checkValidity();
        const feedback = this.form.querySelector(
            `#${field.id} ~ .invalid-feedback`,
        );
        if (!isValid) {
            field.classList.add("is-invalid");
            feedback.textContent = field.validationMessage;
            return;
        }
        return field.classList.remove("is-invalid");
    }

    displayFormMessages(messages) {
        this.clearFormMessagesList();
        messages.forEach((message) => {
            const listItem = document.createElement("li");
            listItem.textContent = message;
            this.formMessagesList.appendChild(listItem);
        });
        this.formMessagesList.classList.remove("d-none");
    }

    displayFormErrors(errors) {
        this.formMessagesList.classList.remove("text-success");
        this.formMessagesList.classList.add("text-danger");
        this.displayFormMessages(errors);
    }

    displayFormSuccessMessages(messages) {
        this.formMessagesList.classList.add("text-success");
        this.formMessagesList.classList.remove("text-danger");
        this.displayFormMessages(messages);
    }

    scrollFieldIntoView(field, fieldLabel) {
        try {
            fieldLabel.scrollIntoView();
        } catch (error) {
            console.error(error);
            field.scrollIntoView();
        }
    }

    displayValidationMessagesForField(fieldName, messages, scrollIntoView) {
        if (fieldName === "__all__") return;
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        if (!field) {
            return;
        }
        const fieldLabel = this.form.querySelector(`label[for="${field.id}"]`);
        const fieldFeedbackElement = this.form.querySelector(
            `#${field.id} ~ .invalid-feedback`,
        );
        // Scroll to first field with feedback
        if (scrollIntoView) {
            this.scrollFieldIntoView(field, fieldLabel);
        }
        const fieldFeedbackList = document.createElement("ul");
        fieldFeedbackList.classList.add("mb-0", "p-0", "list-unstyled");
        for (const messageData of messages) {
            const errorItem = document.createElement("li");
            errorItem.textContent = messageData.message;
            fieldFeedbackList.appendChild(errorItem);
        }
        fieldFeedbackElement.appendChild(fieldFeedbackList);
        field.classList.add("is-invalid");
    }

    displayValidationMessages(validationMessages) {
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
            this.displayValidationMessagesForField(
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
        this.displayFormErrors(
            validationMessages.__all__.map(
                (messageData) => messageData.message,
            ),
        );
    }

    clearFormMessagesList() {
        this.formMessagesList.replaceChildren();
    }

    clearFormAndFieldValidationMessages() {
        this.clearFormMessagesList();
        const allNotEmptyInvalidFeedbackElements = this.form.querySelectorAll(
            ".invalid-feedback:not(:empty)",
        );
        allNotEmptyInvalidFeedbackElements.forEach((element) => {
            element.replaceChildren();
        });
    }

    resetInvalidFields() {
        const invalidFields = this.form.querySelectorAll(".is-invalid");
        invalidFields.forEach((field) => {
            field.classList.remove("is-invalid");
        });
    }
}

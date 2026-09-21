export class EditorValidator {
    constructor(form) {
        this.form = form;
        this.fields = form.querySelectorAll("input, select, textarea");
        this.formMessagesList = form.querySelector(".form-messages-list") || document.querySelector(`[data-form="${form.getAttribute("id")}"]`);
    }

    getFeedbackElementForField(fieldElement, fieldWrapperElement) {
        let fieldFeedbackElement = this.form.querySelector(
            `#${fieldElement.id} ~ .invalid-feedback`,
        );
        if (!fieldFeedbackElement && fieldWrapperElement) {
            fieldFeedbackElement = this.form.querySelector(
                `.field-wrapper[data-field-id="${fieldElement.id}"] ~ .invalid-feedback`,
            );
        }
        return fieldFeedbackElement;
    }

    setupInlineValidation() {
        this.fields.forEach((field) => {
            field.addEventListener("input", (event) => {
                this.validateField(event);
            });
        });
    }

    validateField(event) {
        /**
         * Checks validity of a field and displays the
         * validation message, if any.
         */
        const field = event.currentTarget;
        const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${field.id}"]`);
        const isValid = field.checkValidity();
        const feedback = this.getFeedbackElementForField(field, fieldWrapper);
        if (!isValid) {
            if (fieldWrapper) {
                fieldWrapper.classList.add("is-invalid");
            }
            field.classList.add("is-invalid");
            feedback.textContent = field.validationMessage;
            return;
        }
        if (fieldWrapper) {
            fieldWrapper.classList.remove("is-invalid");
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
        this.displayFormMessages(errors);
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
        const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${field.id}"]`);
        const fieldLabel = this.form.querySelector(`label[for="${field.id}"]`);
        const fieldFeedbackElement = this.getFeedbackElementForField(field, fieldWrapper);
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
        if (fieldWrapper) {
            fieldWrapper.classList.add("is-invalid");
        }
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
        this.formMessagesList.classList.add("d-none");
    }

    clearFieldValidationMessages(fieldElement) {
        const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${field.id}"]`);
        const invalidFeedbackElement = this.getFeedbackElementForField(field, fieldWrapper);
        if (!invalidFeedbackElement) return;
        invalidFeedbackElement.replaceChildren();
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

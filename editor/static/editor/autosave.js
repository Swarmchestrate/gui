import { EditorValidator } from "/static/editor/validation.js";

class EmptyStatusIndicator {
    showLoadingState() {
    }

    showSuccessState() {
    }

    showErrorState() {
    }

    showDefaultState() {
    }
}

class StatusIndicator {
    constructor(statusIndicatorElement) {
        this.statusIndicatorElement = statusIndicatorElement;
        this.defaultInnerHtml = statusIndicatorElement.innerHTML;
        this.loadingHtml = '<span class="spinner-border spinner-border-sm text-body-tertiary" role="status"></span>';
        this.successHtml = '<i class="bi bi-check-lg text-success"></i>';
        this.errorHtml = '<i class="bi bi-x-lg text-danger"></i>';
    }

    showLoadingState() {
        if (this.statusIndicatorElement.innerHTML === this.loadingHtml) {
            return;
        }
        this.statusIndicatorElement.innerHTML = this.loadingHtml;
    }

    showSuccessState() {
        this.statusIndicatorElement.innerHTML = this.successHtml;
    }

    showErrorState() {
        this.statusIndicatorElement.innerHTML = this.errorHtml;
    }

    showDefaultState() {
        this.statusIndicatorElement.innerHTML = this.defaultInnerHtml;
    }
}

export class AsyncFormHandler {
    constructor(form, options) {
        this.form = form;
        if (typeof options !== "object") {
            options = {};
        }
        if (!("onSuccess" in options)) {
            options.onSuccess = () => {};
        }
        this.onSuccess = options.onSuccess;
        this.validator = new EditorValidator(this.form);
        this.validator.setupInlineValidation();
        this.delayedSaves = {};
        this.form.addEventListener("submit", async (event) => {
            // Disable default form submission - fields are sent
            // individually.
            event.preventDefault();
            return false;
        });
        const fields = Array.from(this.form.querySelectorAll("input, select, textarea"));
        fields.forEach(field => {
            // Get the status indicator element for the field
            // that has been edited.
            let statusIndicator = new EmptyStatusIndicator();
            const statusIndicatorElement = document.querySelector(
                `.status-indicator[data-for="${field.id}"]`
            );
            if (statusIndicatorElement) {
                statusIndicator = new StatusIndicator(statusIndicatorElement);
            }
            field.addEventListener("input", () => {
                this.saveDelayed(field, statusIndicator);
            });
        });
    }

    saveDelayed(field, statusIndicator) {
        statusIndicator.showLoadingState();
        const existingDelayedSave = this.delayedSaves[field.id];
        if (existingDelayedSave) {
            window.clearTimeout(existingDelayedSave);
        }
        this.delayedSaves[field.id] = window.setTimeout(() => {
            const body = this.generateRequestBody(field);
            this.sendFieldChanges(body, field, statusIndicator);
        }, 500);
    }

    generateRequestBody(fieldElement) {
        const csrfMiddlewareTokenInputElement = this.form.querySelector(
            "input[name='csrfmiddlewaretoken']"
        );
        const body = new URLSearchParams();
        body.append(
            csrfMiddlewareTokenInputElement.getAttribute("name"),
            csrfMiddlewareTokenInputElement.value
        );
        body.append(
            fieldElement.getAttribute("name"),
            fieldElement.value
        );
        return body;
    }

    async sendFieldChanges(body, fieldElement, statusIndicator) {
        // Request headers
        const headers = new Headers();
        headers.append("Accept", "application/json");

        const response = await fetch(this.form.action, {
            method: "POST",
            headers: headers,
            body: body,
        });

        let responseText;
        let responseData;
        try {
            responseText = await response.text();
        } catch (error) {
            console.error(error);
            statusIndicator.showErrorState();
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            return false;
        }

        try {
            responseData = JSON.parse(responseText);
        } catch (error) {
            console.error(error);
            console.error(responseText);
            statusIndicator.showErrorState();
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            return false;
        }

        if (response.ok) {
            statusIndicator.showSuccessState();
            this.onSuccess(responseData);
            return responseData;
        }

        statusIndicator.showErrorState();
        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
        return false;
    }
}

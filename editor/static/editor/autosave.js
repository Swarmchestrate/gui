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
        this.successHtml = '<i class="bi bi-check2 text-success" aria-hidden="true"></i>';
        this.errorHtml = '<i class="bi bi-x-lg text-danger" aria-hidden="true"></i>';
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

class GlobalStatusIndicator extends StatusIndicator {
    constructor(statusIndicatorElement) {
        super(statusIndicatorElement);
        this.successHtml = '<i class="bi bi-cloud-check" aria-hidden="true"></i>';
        this.errorHtml = '<i class="bi bi-arrow-repeat" aria-hidden="true"></i> Retry';
    }

    updateState(failedSaves) {
        if (failedSaves.length === 0) {
            this.statusIndicatorElement.removeAttribute("data-status");
            return this.showSuccessState();
        }
        this.statusIndicatorElement.dataset.status = "serverError";
        return this.showErrorState();
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
        const globalStatusIndicatorButton = document.querySelector(
            `#${this.form.dataset.categoryIdBase}-tab-pane .global-status-indicator`
        );
        this.globalStatusIndicator = new GlobalStatusIndicator(globalStatusIndicatorButton);
        this.scheduledSaves = {};
        this.failedSaves = [];
        this.form.addEventListener("submit", (event) => {
            // Disable default form submission - fields are sent
            // individually.
            event.preventDefault();
            return false;
        });
        globalStatusIndicatorButton.addEventListener("click", async () => {
            if (!globalStatusIndicatorButton.hasAttribute("data-status")) {
                return;
            }
            await this.retrySaves();
        });
        const fields = Array.from(this.form.querySelectorAll("input, select, textarea"));
        fields.forEach(field => {
            // Get the status indicator element for the field
            // that has been edited.
            const statusIndicator = this.getStatusIndicatorForField(field);
            field.addEventListener("input", () => {
                this.scheduleSave(field, statusIndicator);
            });
        });
    }

    scheduleSave(field, statusIndicator) {
        // Add a short delay before saving a change - if further changes
        // happen within the short delay, then the scheduled save is
        // cancelled and rescheduled. Helps to prevent too many saves being
        // sent at once.
        statusIndicator.showLoadingState();
        this.globalStatusIndicator.showLoadingState();
        const existingScheduledSave = this.scheduledSaves[field.id];
        if (existingScheduledSave) {
            window.clearTimeout(existingScheduledSave);
        }
        this.scheduledSaves[field.id] = window.setTimeout(async () => {
            const body = this.generateRequestBody([field]);
            await this.sendFieldChanges(body, {
                onSuccess: (responseData) => {
                    // Remove field from scheduled saves so it doesn't
                    // get re-saved if we need to retry saving some fields.
                    this.failedSaves = this.failedSaves.filter(fieldId => fieldId != field.id);
                    delete this.scheduledSaves[field.id];
                    this.onSuccess(responseData);
                    statusIndicator.showSuccessState();
                    this.globalStatusIndicator.updateState(this.failedSaves);
                },
                onServerError: () => {
                    this.failedSaves.push(field.id);
                    statusIndicator.showErrorState();
                    this.globalStatusIndicator.updateState(this.failedSaves);
                },
                onValidationError: () => {
                    statusIndicator.showErrorState();
                    this.globalStatusIndicator.updateState(this.failedSaves);
                },
            });
        }, 500);
    }

    async retrySaves() {
        const fieldIdsRetried = [];
        const fieldsToSave = [];
        const statusIndicators = [];
        this.failedSaves.forEach(fieldId => {
            const field = document.querySelector(`#${fieldId}`);
            if (!field) return;
            const statusIndicator = this.getStatusIndicatorForField(field);
            fieldIdsRetried.push(fieldId);
            fieldsToSave.push(field);
            statusIndicators.push(statusIndicator);
        });
        const body = this.generateRequestBody(fieldsToSave);
        this.sendFieldChanges(body, {
            onSuccess: () => {
                this.failedSaves = this.failedSaves.filter(fieldId => !fieldIdsRetried.includes(fieldId));
                statusIndicators.forEach(statusIndicator => {
                    statusIndicator.showSuccessState();
                });
                this.globalStatusIndicator.updateState(this.failedSaves);
            },
            onServerError: () => {
                this.globalStatusIndicator.updateState(this.failedSaves);
            },
        });
    }

    generateRequestBody(fieldElements) {
        const csrfMiddlewareTokenInputElement = this.form.querySelector(
            "input[name='csrfmiddlewaretoken']"
        );
        const body = new URLSearchParams();
        body.append(
            csrfMiddlewareTokenInputElement.getAttribute("name"),
            csrfMiddlewareTokenInputElement.value
        );
        fieldElements.forEach(fieldElement => {
            body.append(
                fieldElement.getAttribute("name"),
                fieldElement.value
            );
        });
        return body;
    }

    async sendFieldChanges(body, options) {
        if (typeof options !== "object") {
            options = {};
        }
        if (!("onSuccess" in options)) {
            options.onSuccess = () => {};
        }
        if (!("onServerError" in options)) {
            options.onServerError = () => {};
        }
        if (!("onValidationError" in options)) {
            options.onValidationError = () => {};
        }
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
            console.error("Did not receive expected JSON response.");
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            options.onServerError();
            return false;
        }

        try {
            responseData = JSON.parse(responseText);
        } catch (error) {
            console.error(error);
            console.error(response.status, response.statusText);
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            options.onServerError();
            return false;
        }

        if (response.ok) {
            options.onSuccess(responseData);
            return responseData;
        }

        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
        return false;
    }

    // Utility methods
    getStatusIndicatorForField(field) {
        const statusIndicatorElement = document.querySelector(
            `.status-indicator[data-for="${field.id}"]`
        );
        if (!statusIndicatorElement) {
            return new EmptyStatusIndicator();
        }
        return new StatusIndicator(statusIndicatorElement);
    }
}

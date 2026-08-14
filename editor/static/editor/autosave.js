import {
    EmptyStatusIndicator,
    ErrorSummary,
    GlobalStatusIndicator,
    RetrySaveButton,
    StatusIndicator,
} from "/static/editor/autosave_utils.js";
import { EditorValidator } from "/static/editor/validation.js";

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
        // Fields are saved individually, so no need to submit
        // the actual form.
        this.form.addEventListener("submit", (event) => {
            // Disable default form submission - fields are sent
            // individually.
            event.preventDefault();
            return false;
        });
        // Global status indicator
        const globalStatusIndicatorButton = document.querySelector(
            `#${this.form.dataset.categoryIdBase}-tab-pane .global-status-indicator`
        );
        this.globalStatusIndicator = new GlobalStatusIndicator(globalStatusIndicatorButton);
        // Error summary
        const errorSummaryElement = document.querySelector(
            `#${this.form.dataset.categoryIdBase}-tab-pane .error-details`
        );
        this.errorSummary = new ErrorSummary(errorSummaryElement);
        this.scheduledSaves = {};
        // Retry button - when there are saves that didn't manage to go/may not have
        // gone through.
        const retrySaveButtonElement = document.querySelector(
            `#${this.form.dataset.categoryIdBase}-tab-pane .btn-retry-save`
        );
        retrySaveButtonElement.addEventListener("click", async () => {
            this.globalStatusIndicator.showLoadingState();
            await this.retrySaves();
        });
        this.retrySaveButton = new RetrySaveButton(retrySaveButtonElement);
        // Setting up individual saves.
        this.form.addEventListener("input", (event) => {
            const field = event.target;
            if (field.matches(
                "input[data-maps-to], select[data-maps-to], textarea[data-maps-to]"
            )) {
                // E.g., text array fields map to a hidden input which gets
                // submitted instead of the individual inputs/selects/textareas.
                const hiddenInputId = event.target.dataset.mapsTo;
                const hiddenInput = this.form.querySelector(`#${hiddenInputId}`);
                const statusIndicator = this.getStatusIndicatorForField(hiddenInput);
                return this.scheduleSave(hiddenInput, statusIndicator);
            }
            // Get the status indicator element for the field
            // that has been edited.
            const statusIndicator = this.getStatusIndicatorForField(field);
            return this.scheduleSave(field, statusIndicator);
        });
        // Setting up text array fields.
        this.form.addEventListener("click", (event) => {
            if (!event.target.matches("button[data-maps-to]")) {
                return;
            }
            const hiddenInputId = event.target.dataset.mapsTo;
            const field = this.form.querySelector(`#${hiddenInputId}`);
            const statusIndicator = this.getStatusIndicatorForField(field)
            return this.scheduleSave(field, statusIndicator);
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
            await this.sendFieldChangeIndividually(field, statusIndicator);
        }, 500);
    }

    async sendFieldChangeIndividually(field, statusIndicator) {
        this.validator.clearFieldValidationMessages(field);
        const body = this.generateRequestBody([field]);
        await this.sendFieldChanges(body, {
            onSuccess: (responseData) => {
                // The field just saved successfully, so remove it from the global status
                // indicator's error summary. We don't need to worry if the field was removed
                // from the database schema, as the generated form would be empty and shouldn't
                // reach onSuccess().
                this.globalStatusIndicator.clearIssuesForField(field);
                this.errorSummary.clearIssuesForField(field);
                this.retrySaveButton.updateVisibility(this.globalStatusIndicator.savesToRetry);
                delete this.scheduledSaves[field.id];
                this.onSuccess(responseData);
                statusIndicator.showSuccessState();
                this.globalStatusIndicator.updateState();
                this.errorSummary.updateState();
            },
            onNetworkError: () => {
                this.globalStatusIndicator.savesToRetry.add(field.id);
                this.errorSummary.savesToRetry.add(field.id);
                this.retrySaveButton.updateVisibility(this.globalStatusIndicator.savesToRetry);
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState({ focusOnError: true });
                this.errorSummary.updateState();
            },
            onValidationError: (responseData) => {
                this.globalStatusIndicator.invalidFields.add(field.id);
                this.errorSummary.invalidFields.add(field.id);
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState();
                this.errorSummary.updateState();
            },
            onUnavailableFieldsError: (responseData) => {
                responseData.unavailable_fields.forEach(fieldName => {
                    this.globalStatusIndicator.unavailableFields.add(
                        fieldName
                    );
                    this.errorSummary.unavailableFields.add(
                        fieldName
                    );
                });
                this.validator.displayValidationMessagesForField(
                    field.getAttribute("name"),
                    [{ message: "This field appears to have been removed from the SAT/CDT specification. Changes won't be saved unless the field is re-added." }]
                );
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState({ focusOnError: true });
                this.errorSummary.updateState();
            },
            onServerError: () => {
                this.globalStatusIndicator.savesToRetry.add(field.id);
                this.errorSummary.savesToRetry.add(field.id);
                this.retrySaveButton.updateVisibility(this.globalStatusIndicator.savesToRetry);
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState({ focusOnError: true });
                this.errorSummary.updateState();
            },
        });
    }

    async retrySaves() {
        const fieldsToSave = {};
        this.globalStatusIndicator.savesToRetry.forEach(fieldId => {
            const field = document.querySelector(`#${fieldId}`);
            if (!field) return;
            const statusIndicator = this.getStatusIndicatorForField(field);
            fieldsToSave[fieldId] = {
                fieldElement: field,
                statusIndicator: statusIndicator,
            };
        });
        const individualSaves = [];
        for (const fieldId in fieldsToSave) {
            const fieldElement = fieldsToSave[fieldId].fieldElement;
            const statusIndicator = fieldsToSave[fieldId].statusIndicator;
            individualSaves.push(
                this.sendFieldChangeIndividually(fieldElement, statusIndicator)
            );
        }
        await Promise.all(individualSaves);
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
        if (!("onNetworkError" in options)) {
            options.onNetworkError = () => {};
        }
        if (!("onServerError" in options)) {
            options.onServerError = () => {};
        }
        if (!("onValidationError" in options)) {
            options.onValidationError = () => {};
        }
        if (!("onUnavailableFieldsError" in options)) {
            options.onUnavailableFieldsError = () => {};
        }
        // Request headers
        const headers = new Headers();
        headers.append("Accept", "application/json");

        let response;
        try {
            response = await fetch(this.form.action, {
                method: "POST",
                headers: headers,
                body: body,
            });
        } catch (error) {
            console.error(error);
            const isNetworkError = error.message.startsWith("NetworkError");
            if (error instanceof TypeError && isNetworkError) {
                return options.onNetworkError();
            }
            return options.onServerError();
        }

        let responseText;
        let responseData;
        try {
            responseText = await response.text();
        } catch (error) {
            console.error(error);
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            options.onServerError();
            return false;
        }

        try {
            responseData = JSON.parse(responseText);
        } catch (error) {
            console.error("Did not receive expected JSON response.");
            console.error(response.status, response.statusText);
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            options.onServerError();
            return false;
        }

        if (Object.hasOwn(responseData, "unavailable_fields")) {
            options.onUnavailableFieldsError(responseData);
        }

        if (response.ok) {
            options.onSuccess(responseData);
            return responseData;
        }

        if (response.status === 422) {
            return false;
        }

        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
        options.onValidationError(responseData);
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

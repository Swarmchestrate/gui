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
        this.successHtml = '<i class="bi bi-database-check" aria-hidden="true"></i>';
        this.errorHtml = '<i class="bi bi-database-exclamation" aria-hidden="true"></i>';
        this.popover = new bootstrap.Popover(statusIndicatorElement, {
            title: `<span class="lh-1 fs-5">${this.successHtml}</span> Status`,
            content: "Content",
            html: true,
            trigger: "focus",
        });
        this.savesToRetry = [];
        this.unavailableFields = [];
        this.invalidFields = [];
        this.showSuccessState();
    }

    #getFailedSavesErrorSummary() {
        if (this.savesToRetry.length === 0) {
            return "";
        }
        const retryButtonIcon = `
            <span class="d-inline-block bg-light rounded px-2 py-1">
                <i class="bi bi-arrow-repeat" aria-hidden="true"></i> Retry
            </span>
        `;
        return `<div>
            <strong>Some changes may not have been saved.</strong>
            Try saving them again using the ${retryButtonIcon} button.
        </div>`;
    }

    #generateJumpToList(fieldIds) {
        const listElement = document.createElement("UL");
        listElement.classList.add("mb-0");
        fieldIds.forEach(fieldId => {
            const listItemElement = document.createElement("LI");
            const field = document.querySelector(`#${fieldId}`);
            if (!field) {
                listItemElement.textContent = fieldId;
                return listElement.appendChild(listItemElement);
            }
            const anchorElement = document.createElement("A");
            anchorElement.textContent = field.getAttribute("name").trim();
            anchorElement.setAttribute("href", `#${field.id}`);
            const fieldLabel = document.querySelector(
                `label[for="${field.id}"], .label[for="${field.id}"]`
            );
            if (!fieldLabel) {
                listItemElement.appendChild(anchorElement);
                return listElement.appendChild(listItemElement);
            }
            anchorElement.textContent = fieldLabel.textContent.trim();
            if (fieldLabel.hasAttribute("id")) {
                anchorElement.setAttribute("href", `#${fieldLabel.id}`);
            }
            listItemElement.appendChild(anchorElement);
            return listElement.appendChild(listItemElement);
        });
        return listElement.outerHTML;
    }

    #getInvalidFieldsErrorSummary() {
        if (this.invalidFields.length === 0) {
            return "";
        }
        const jumpToListHtml = this.#generateJumpToList(this.invalidFields);
        return `<div>
            <strong>Some fields require changes:</strong>
            ${jumpToListHtml}
        </div>`;
    }

    #getUnavailableFieldsErrorSummary() {
        if (this.unavailableFields.length === 0) {
            return "";
        }
        const jumpToListHtml = this.#generateJumpToList(this.unavailableFields.map(fieldName => `id_${fieldName}`));
        return `<div>
            <strong>Some fields appear to have been removed from the database schema:</strong>
            ${jumpToListHtml}
        </div>`;
    }

    #generateSummaryForPopoverBody() {
        let summary = document.createElement("div");
        summary.classList.add("d-flex", "flex-column", "row-gap-2");
        summary.innerHTML = `
            ${this.#getFailedSavesErrorSummary()}
            ${this.#getInvalidFieldsErrorSummary()}
            ${this.#getUnavailableFieldsErrorSummary()}
        `;
        return summary;
    }

    showSuccessState() {
        super.showSuccessState();
        this.popover.setContent({
            ".popover-header": "All changes saved",
            ".popover-body": "Changes are automatically saved to the database.",
        });
    }

    showLoadingState() {
        super.showLoadingState();
        this.popover.setContent({
            ".popover-header": "Saving...",
            ".popover-body": "Changes are currently being saved to the database.",
        });
    }

    showErrorState() {
        super.showErrorState();
        this.popover.setContent({
            ".popover-header": "Some things need attention",
            ".popover-body": this.#generateSummaryForPopoverBody(),
        });
        this.statusIndicatorElement.focus();
    }

    updateState() {
        if (
            this.invalidFields.length === 0
            && this.unavailableFields.length === 0
            && this.savesToRetry.length === 0
        ) {
            return this.showSuccessState();
        }
        this.showErrorState();
    }

    // Utility methods
    addSavesToRetry(fieldIds) {
        this.savesToRetry.push(...fieldIds);
        this.savesToRetry = [...new Set(this.savesToRetry)];
    }

    addInvalidFields(fieldIds) {
        this.invalidFields.push(...fieldIds);
        this.invalidFields = [...new Set(this.invalidFields)];
    }

    addUnavailableFields(fieldNames) {
        this.unavailableFields.push(...fieldNames);
        this.unavailableFields = [...new Set(this.unavailableFields)];
    }

    removeFieldsFromFailedSavesErrorSummary(fieldIds) {
        this.savesToRetry = this.savesToRetry.filter(fieldId => !fieldIds.includes(fieldId));
    }

    removeFieldsFromInvalidFieldsErrorSummary(fieldIds) {
        this.invalidFields = this.invalidFields.filter(fieldId => !fieldIds.includes(fieldId));
    }
    
    removeFieldsFromUnavailableFieldsErrorSummary(fieldNames) {
        this.unavailableFields = this.unavailableFields.filter(fieldName => !fieldNames.includes(fieldName));
    }

    removeFieldsFromErrorSummary(fieldsToRemove) {
        const fieldIdsToRemove = fieldsToRemove.map(field => field.id);
        const fieldNamesToRemove = fieldsToRemove.map(field => field.getAttribute("name"));
        this.removeFieldsFromFailedSavesErrorSummary(fieldIdsToRemove);
        this.removeFieldsFromInvalidFieldsErrorSummary(fieldIdsToRemove);
        this.removeFieldsFromUnavailableFieldsErrorSummary(fieldNamesToRemove);
    }
}

class RetrySaveButton {
    constructor(buttonElement, onClickAction) {
        this.buttonElement = buttonElement;
    }

    show() {
        this.buttonElement.classList.remove("d-none");
    }

    hide() {
        this.buttonElement.classList.add("d-none");
    }

    updateVisibility(savesToRetry) {
        if (savesToRetry.length > 0) {
            return this.show();
        }
        return this.hide();
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
        const body = this.generateRequestBody([field]);
        await this.sendFieldChanges(body, {
            onSuccess: (responseData) => {
                // The field just saved successfully, so remove it from the global status
                // indicator's error summary. We don't need to worry if the field was removed
                // from the database schema, as the generated form would be empty and shouldn't
                // reach onSuccess().
                this.globalStatusIndicator.removeFieldsFromErrorSummary([field]);
                this.retrySaveButton.updateVisibility(this.globalStatusIndicator.savesToRetry);
                delete this.scheduledSaves[field.id];
                this.onSuccess(responseData);
                statusIndicator.showSuccessState();
                this.globalStatusIndicator.updateState();
            },
            onNetworkError: () => {
                this.globalStatusIndicator.addSavesToRetry([field.id]);
                this.retrySaveButton.updateVisibility(this.globalStatusIndicator.savesToRetry);
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState();
            },
            onValidationError: (responseData) => {
                this.globalStatusIndicator.addInvalidFields([field.id]);
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState();
            },
            onUnavailableFieldsError: (responseData) => {
                this.globalStatusIndicator.addUnavailableFields(
                    responseData.unavailable_fields
                );
                this.validator.displayValidationMessagesForField(
                    field.getAttribute("name"),
                    [{ message: "This field appears to have been removed from the database schema." }]
                );
                statusIndicator.showErrorState();
                this.globalStatusIndicator.updateState();
            },
            onServerError: () => {
                this.globalStatusIndicator.addSavesToRetry([field.id]);
                this.retrySaveButton.updateVisibility();
                statusIndicator.showErrorState();
                this.globalStatusIndicator.showErrorState();
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

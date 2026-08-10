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
            trigger: "focus"
        });
        this.showSuccessState();
    }

    updateState(failedSaves) {
        if (failedSaves.length === 0) {
            this.statusIndicatorElement.removeAttribute("data-status");
            return this.showSuccessState();
        }
        return this.showNetworkErrorState();
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

    showNetworkErrorState() {
        super.showErrorState();
        const retryButtonIcon = `
            <span class="d-inline-block bg-light rounded px-2 py-1">
                <i class="bi bi-arrow-repeat" aria-hidden="true"></i> Retry
            </span>
        `;
        this.popover.setContent({
            ".popover-header": "Some changes may not have been saved",
            ".popover-body": `An error with the network may have caused some changes to not be saved. Try saving them again using the ${retryButtonIcon} button.`,
        });
        this.statusIndicatorElement.focus();
    }

    #generateJumpToList(fieldNames) {
        const listElement = document.createElement("UL");
        listElement.classList.add("mb-0");
        fieldNames.forEach(fieldName => {
            const listItemElement = document.createElement("LI");
            const field = document.querySelector(`[name=${fieldName}]`);
            if (!field) {
                listItemElement.textContent = fieldName;
                return listElement.appendChild(listItemElement);
            }
            const fieldLabel = document.querySelector(
                `label[for="${field.id}"], .label[for="${field.id}"]`
            );
            if (!fieldLabel) {
                listItemElement.textContent = fieldName;
                return listElement.appendChild(listItemElement);
            }
            const anchorElement = document.createElement("A");
            anchorElement.textContent = fieldLabel.textContent.trim();
            anchorElement.setAttribute("href", `#${field.id}`);
            if (fieldLabel.hasAttribute("id")) {
                anchorElement.setAttribute("href", `#${fieldLabel.id}`);
            }
            listItemElement.appendChild(anchorElement);
            return listElement.appendChild(listItemElement);
        });
        return listElement.outerHTML;
    }

    showValidationErrorState(responseData) {
        super.showErrorState();
        const jumpToListHtml = this.#generateJumpToList(Object.keys(
            responseData.feedback
        ));
        this.popover.setContent({
            ".popover-header": "Some fields need some adjustments",
            ".popover-body": `<p>See the feedback displayed by relevant fields on what to change.</p> Go to a field: ${jumpToListHtml}`,
        });
        this.statusIndicatorElement.focus();
    }

    showErrorState() {
        super.showErrorState();
        this.popover.setContent({
            ".popover-header": "Something happened",
            ".popover-body": "The latest changes may not have been saved. Please make a report of the problem at the Swarmchestrate GUI issue tracker.",
        });
        this.statusIndicatorElement.focus();
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
        const retrySaveButtonElement = document.querySelector(
            `#${this.form.dataset.categoryIdBase}-tab-pane .btn-retry-save`
        );
        retrySaveButtonElement.addEventListener("click", async () => {
            this.globalStatusIndicator.showLoadingState();
            await this.retrySaves();
        });
        this.retrySaveButton = new RetrySaveButton(retrySaveButtonElement);
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
                    this.retrySaveButton.hide();
                },
                onNetworkError: () => {
                    this.failedSaves.push(field.id);
                    statusIndicator.showErrorState();
                    this.globalStatusIndicator.updateState(this.failedSaves);
                    this.retrySaveButton.show();
                },
                onValidationError: (responseData) => {
                    statusIndicator.showErrorState();
                    this.globalStatusIndicator.showValidationErrorState(responseData);
                },
                onServerError: () => {
                    statusIndicator.showErrorState();
                    this.globalStatusIndicator.showErrorState();
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
                this.retrySaveButton.hide();
            },
            onNetworkError: () => {
                this.globalStatusIndicator.updateState(this.failedSaves);
                this.retrySaveButton.show();
            },
            onValidationError: (responseData) => {
                this.globalStatusIndicator.showValidationErrorState(responseData);
            },
            onServerError: () => {
                this.globalStatusIndicator.showErrorState();
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
        if (!("onNetworkError" in options)) {
            options.onNetworkError = () => {};
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

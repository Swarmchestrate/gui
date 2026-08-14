export class EmptyStatusIndicator {
    showLoadingState() {
    }

    showSuccessState() {
    }

    showErrorState() {
    }

    showDefaultState() {
    }
}

export class StatusIndicator {
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

export class GlobalStatusIndicator extends StatusIndicator {
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
        this.savesToRetry = new Set();
        this.unavailableFields = new Set();
        this.invalidFields = new Set();
        this.showSuccessState();
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

    showErrorState(focusOnError) {
        super.showErrorState();
        this.popover.setContent({
            ".popover-header": "Issues found",
            ".popover-body": "Please expand details of the issues below.",
        });
        if (!focusOnError) return;
        this.statusIndicatorElement.focus();
    }

    updateState(options) {
        if (typeof options !== "object") {
            options = {};
        }
        if (!("focusOnError" in options)) {
            options.focusOnError = false;
        }
        if (
            this.invalidFields.size === 0
            && this.unavailableFields.size === 0
            && this.savesToRetry.size === 0
        ) {
            return this.showSuccessState();
        }
        this.showErrorState(options.focusOnError);
    }

    // Utility methods
    clearIssuesForField(field) {
        this.savesToRetry.delete(field.id);
        this.invalidFields.delete(field.id);
        this.unavailableFields.delete(field.getAttribute("name"));
    }
}

export class ErrorSummary {
    constructor(detailsElement) {
        this.detailsElement = detailsElement;
        this.savesToRetry = new Set();
        this.unavailableFields = new Set();
        this.invalidFields = new Set();
    }

    #generateJumpToList(fieldIds) {
        const listElement = document.createElement("UL");
        listElement.classList.add("mb-0");
        fieldIds.forEach(fieldId => {
            const listItemElement = document.createElement("LI");
            // Try to set up the jump link using just the field first.
            const field = document.querySelector(`#${fieldId}`);
            if (!field) {
                listItemElement.textContent = fieldId;
                return listElement.appendChild(listItemElement);
            }
            const anchorElement = document.createElement("A");
            anchorElement.textContent = field.getAttribute("name").trim();
            anchorElement.setAttribute("href", `#${field.id}`);
            const isFieldHidden = (
                field.getAttribute("aria-hidden") === "true"
                || field.getAttribute("type") === "hidden"
            );
            // If the field is hidden then the jump link won't work, so need
            // to attempt to find a corresponding visible element.
            if (isFieldHidden) {
                const alternativeElement = document.querySelector(
                    `[data-maps-to="${field.id}"]`
                );
                if (alternativeElement && alternativeElement.hasAttribute("id")) {
                    anchorElement.setAttribute("href", `#${alternativeElement.id}`);
                }
            }
            // If there is a corresponding label (which there should), then
            // the jump link can become more descriptive.
            const fieldLabel = document.querySelector(
                `label[for="${field.id}"], .label[for="${field.id}"]`
            );
            if (!fieldLabel) {
                listItemElement.appendChild(anchorElement);
                return listElement.appendChild(listItemElement);
            }
            if (fieldLabel.textContent.trim()) {
                anchorElement.textContent = fieldLabel.textContent.trim()
            }
            if (fieldLabel.hasAttribute("id")) {
                anchorElement.setAttribute("href", `#${fieldLabel.id}`);
            }
            listItemElement.appendChild(anchorElement);
            return listElement.appendChild(listItemElement);
        });
        return listElement.outerHTML;
    }

    #generateSavesToRetrySection() {
        if (this.savesToRetry.size === 0) {
            return "";
        }
        const retryButtonIcon = `
            <span class="d-inline-block bg-light rounded px-2 py-1">
                <i class="bi bi-arrow-repeat" aria-hidden="true"></i> Retry
            </span>
        `;
        return `<div class="alert alert-warning m-0">
            <strong>Some changes may not have been saved.</strong>
            Try saving them again using the ${retryButtonIcon} button.
        </div>`;
    }

    #generateInvalidFieldsSection() {
        if (this.invalidFields.size === 0) {
            return "";
        }
        const jumpToListHtml = this.#generateJumpToList(this.invalidFields);
        return `<div class="alert alert-warning m-0">
            <strong>Changes to these fields won't be saved until the highlighted issues are addressed:</strong>
            ${jumpToListHtml}
        </div>`;
    }

    #generateUnavailableFieldsSection() {
        if (this.unavailableFields.size === 0) {
            return "";
        }
        const jumpToListHtml = this.#generateJumpToList(Array.from(this.unavailableFields).map(fieldName => `id_${fieldName}`));
        return `<div class="alert alert-warning m-0">
            <strong>Some fields have been removed from the SAT/CDT specification:</strong>
            ${jumpToListHtml}
            <p class="mt-2 mb-0">It won't be possible to save changes to these fields unless they are re-added.</p>
        </div>`;
    }

    #generate() {
        let errorSummaryElement = document.createElement("div");
        errorSummaryElement.classList.add(
            "d-flex",
            "error-summary",
            "flex-column",
            "row-gap-2",
            "pt-2"
        );
        errorSummaryElement.innerHTML = `
            ${this.#generateSavesToRetrySection()}
            ${this.#generateInvalidFieldsSection()}
            ${this.#generateUnavailableFieldsSection()}
        `;
        return errorSummaryElement;
    }

    show() {
        const previousErrorSummaryElement = this.detailsElement.querySelector(".error-summary");
        if (previousErrorSummaryElement) {
            previousErrorSummaryElement.remove();
        }
        const errorSummaryElement = this.#generate();
        const numProblems = [
            this.savesToRetry,
            this.invalidFields,
            this.unavailableFields,
        ].filter(fields => fields.size > 0).length;
        this.detailsElement.querySelector("summary").innerHTML = `
            <i class="bi bi-exclamation-circle me-1"></i>
            ${numProblems} ${(numProblems === 1) ? "problem" : "problems"}
        `;
        this.detailsElement.appendChild(errorSummaryElement);
        this.detailsElement.removeAttribute("open");
        this.detailsElement.classList.remove("d-none");
    }
    
    hide() {
        this.detailsElement.classList.add("d-none");
    }

    updateState() {
        if (
            this.invalidFields.size === 0
            && this.unavailableFields.size === 0
            && this.savesToRetry.size === 0
        ) {
            return this.hide();
        }
        this.show();
    }

    // Utility methods
    clearIssuesForField(field) {
        this.savesToRetry.delete(field.id);
        this.invalidFields.delete(field.id);
        this.unavailableFields.delete(field.getAttribute("name"));
    }
}

export class RetrySaveButton {
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
        if (savesToRetry.size > 0) {
            return this.show();
        }
        return this.hide();
    }
}
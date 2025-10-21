import { EditorValidator } from "/static/editor/validation.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";

export class EditorForm {
    constructor(form, options) {
        this.form = form;
        if (typeof options != "object") {
            options = {};
        }
        if (!("onSubmit" in options)) {
            options.onSubmit = () => {};
        }
        this.onSubmit = options.onSubmit;
        this.validator = new EditorValidator(this.form);
        this.form.addEventListener("submit", async (event) => {
            this.runSubmitActions();
            return false;
        });
        if (!("useStatusButton" in options)) {
            options.useStatusButton = true;
        }
        if (!("formStatusButtonSelector" in options)) {
            options.formStatusButtonSelector = "button[type='submit']";
        }
        if (!options.useStatusButton) {
            return;
        }
        this.formStatusButton = form.querySelector(
            options.formStatusButtonSelector,
        );
        this.formStatusButtonLoadingText =
            this.formStatusButton.querySelector(".loading-text");
        this.formStatusButtonLoadingSuccessText =
            this.formStatusButton.querySelector(".success-status-text");
        this.formStatusButtonDefaultText =
            this.formStatusButton.querySelector(".default-text");
        this.formStatusButtonStatusText = this.formStatusButton.querySelector(
            ".loading-status-text",
        );
    }

    prepareFormBody() {
        const data = new URLSearchParams();
        for (const pair of new FormData(this.getFormToSubmit())) {
            data.append(pair[0], pair[1]);
        }
        return data;
    }

    getFormToSubmit() {
        return this.form;
    }

    getFormAction() {
        return this.form.action;
    }

    async submitAsynchronously() {
        const body = this.prepareFormBody();
        // Request headers
        const headers = new Headers();
        headers.append("Accept", "application/json");
        this.runSubmitActions();
        const response = await fetch(this.getFormAction(), {
            method: "POST",
            headers: headers,
            body: body,
        });
        let responseData;
        try {
            responseData = await response.json();
        } catch (error) {
            this.hideLoadingText();
            return displayFormErrors([
                "Encountered checking server validation results. Please try again.",
            ]);
        }
        if (response.ok) {
            this.showLoadingSuccessText();
            return this.onSubmit();
        }
        try {
            console.error(await response.text());
        } catch (error) {
            console.error(error);
        }
        this.hideLoadingText();
        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
    }

    runSubmitActions() {
        this.showLoadingText();
        this.validator.resetInvalidFields();
        this.validator.clearFormAndFieldValidationMessages();
    }

    showLoadingText() {
        if (!this.formStatusButton) {
            return;
        }
        this.formStatusButton.disabled = true;
        if (
            !this.formStatusButtonDefaultText ||
            !this.formStatusButtonLoadingText ||
            !this.formStatusButtonLoadingSuccessText
        ) {
            return;
        }
        this.formStatusButtonLoadingText.classList.remove("d-none");
        this.formStatusButtonDefaultText.classList.add("d-none");
        this.formStatusButtonLoadingSuccessText.classList.add("d-none");
    }

    showLoadingSuccessText() {
        if (!this.formStatusButton) {
            return;
        }
        this.formStatusButton.disabled = true;
        if (
            !this.formStatusButtonDefaultText ||
            !this.formStatusButtonLoadingText ||
            !this.formStatusButtonLoadingSuccessText
        ) {
            return;
        }
        this.formStatusButtonLoadingSuccessText.classList.remove("d-none");
        this.formStatusButtonLoadingText.classList.add("d-none");
        this.formStatusButtonDefaultText.classList.add("d-none");
    }

    hideLoadingText() {
        if (!this.formStatusButton) {
            return;
        }
        this.formStatusButton.disabled = false;
        if (
            !this.formStatusButtonDefaultText ||
            !this.formStatusButtonLoadingText ||
            !this.formStatusButtonLoadingSuccessText
        ) {
            return;
        }
        this.formStatusButtonDefaultText.classList.remove("d-none");
        this.formStatusButtonLoadingText.classList.add("d-none");
        this.formStatusButtonLoadingSuccessText.classList.add("d-none");
    }

    updateStatusText(updatedText) {
        if (!this.formStatusButtonStatusText) {
            return;
        }
        this.formStatusButtonStatusText.textContent = updatedText;
    }

    showSuccessText() {
        this.updateStatusText();
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const editorFormElement = document.querySelector("#editor-form");
    const editorForm = new EditorForm(editorFormElement);
    editorForm.validator.setupInlineValidation();
    setupFormsetTables();
});

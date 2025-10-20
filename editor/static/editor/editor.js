import { EditorValidator } from "/static/editor/validation.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";

export class EditorForm {
    constructor(form, options) {
        this.form = form;
        if (typeof options != "object") {
            options = {};
        }
        if (!("formStatusButtonSelector" in options)) {
            options.formStatusButtonSelector = "button[type='submit']";
        }
        if (!("successText" in options)) {
            options.successText = "Redirecting";
        }
        if (!("onSubmit" in options)) {
            options.onSubmit = () => {};
        }
        this.formStatusButton = form.querySelector(
            options.formStatusButtonSelector,
        );
        this.formStatusButtonLoadingText =
            this.formStatusButton.querySelector(".loading-text");
        this.formStatusButtonDefaultText =
            this.formStatusButton.querySelector(".default-text");
        this.formStatusButtonStatusText =
            this.formStatusButton.querySelector(".status-text");
        this.successText = options.successText;
        this.onSubmit = options.onSubmit;
        this.validator = new EditorValidator(this.form);

        this.form.addEventListener("submit", async (event) => {
            this.runSubmitActions();
            return false;
        });
    }

    runSubmitActions() {
        this.showLoadingText();
        this.validator.resetInvalidFields();
        this.validator.clearFormAndFieldValidationMessages();
    }

    showLoadingText() {
        this.formStatusButton.disabled = true;
        if (
            !this.formStatusButtonDefaultText ||
            !this.formStatusButtonLoadingText
        ) {
            return;
        }
        this.formStatusButtonLoadingText.classList.remove("d-none");
        this.formStatusButtonDefaultText.classList.add("d-none");
    }

    hideLoadingText() {
        this.formStatusButton.disabled = false;
        if (
            !this.formStatusButtonDefaultText ||
            !this.formStatusButtonLoadingText
        ) {
            return;
        }
        this.formStatusButtonLoadingText.classList.add("d-none");
        this.formStatusButtonDefaultText.classList.remove("d-none");
    }

    updateStatusText(updatedText) {
        if (!formStatusButtonStatusText) {
            return;
        }
        this.formStatusButtonStatusText.textContent = updatedText;
    }

    showSuccessText() {
        this.updateStatusText();
    }

    async submitAsynchronously() {
        const data = new URLSearchParams();
        for (const pair of new FormData(this.form)) {
            data.append(pair[0], pair[1]);
        }
        // Request headers
        const headers = new Headers();
        headers.append("Accept", "application/json");
        this.runSubmitActions();
        const response = await fetch(this.form.action, {
            method: "POST",
            headers: headers,
            body: data,
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
            this.updateStatusText(this.successText);
            return this.onSubmit();
        }
        this.hideLoadingText();
        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const editorFormElement = document.querySelector("#editor-form");
    const editorForm = new EditorForm(editorFormElement);
    editorForm.validator.setupInlineValidation();
    setupFormsetTables();
});

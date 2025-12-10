import { EditorValidator } from "/static/editor/validation.js";

class AsyncFormSubmissionStatusButton {
    constructor(statusButton) {
        this.statusButton = statusButton;
        this.defaultInnerHtml = statusButton.innerHTML;
        this.successText = "Saved Changes";
        this.loadingHtml = `<span class="spinner-border spinner-border-sm me-1" role="status"></span> Applying Changes`;
    }

    showLoadingState() {
        this.statusButton.disabled = true;
        this.statusButton.innerHTML = this.loadingHtml;
    }

    showDefaultState() {
        this.statusButton.disabled = false;
        this.statusButton.innerHTML = this.defaultInnerHtml;
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
        this.statusButton = new AsyncFormSubmissionStatusButton(
            this.form.querySelector("button[type='submit']"),
        );
        this.form.addEventListener("submit", async (event) => {
            event.preventDefault();
            this.showLoadingState();
            this.submitForm();
            return false;
        });
    }

    showLoadingState() {
        this.statusButton.showLoadingState();
    }

    async submitForm() {
        const body = new URLSearchParams();
        for (const pair of new FormData(this.form)) {
            body.append(pair[0], pair[1]);
        }
        // Request headers
        const headers = new Headers();
        headers.append("Accept", "application/json");
        this.showLoadingState();

        const response = await fetch(this.form.action, {
            method: "POST",
            headers: headers,
            body: body,
        });

        let responseData;
        try {
            const responseText = await response.text();
            responseData = JSON.parse(responseText);
        } catch (error) {
            console.error(error);
            this.statusButton.showDefaultState();
            this.validator.displayFormErrors([
                "Encountered a problem whilst checking server validation results. Please try again.",
            ]);
            return false;
        }

        if (response.ok) {
            this.statusButton.showDefaultState();
            this.onSuccess(responseData);
            return responseData;
        }

        try {
            console.error(await response.text());
        } catch (error) {
            console.error(error);
        }

        this.statusButton.showDefaultState();
        const validationMessages = responseData.feedback || {};
        this.validator.displayValidationMessages(validationMessages);
        return false;
    }
}

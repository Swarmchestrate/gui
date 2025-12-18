import { Dialog } from "/static/dialog.js";
import { AsyncFormHandler } from "/static/editor/async_forms.js";

export class FormDialog extends Dialog {
    constructor(dialog, closeButtons, showButtons, options, form) {
        super(dialog, closeButtons, showButtons, options);
        this.form = form;
        if (!("onFormSuccess" in this.options)) {
            this.options.onFormSuccess = () => {};
        }
        this.onFormSuccess = this.options.onFormSuccess;
        this.asyncFormHandler = new AsyncFormHandler(form, {
            onSuccess: (responseData) => {
                this.onFormSuccess(responseData);
                this.dialog.close();
            },
        });
    }

    isAnyFieldChanged() {
        const inputsAndTextareas =
            this.form.querySelectorAll("input, textarea");
        for (const field of inputsAndTextareas) {
            if (field.value === field.defaultValue) continue;
            if (!field.value && !field.defaultValue) continue;
            return true;
        }
        const selects = this.form.querySelectorAll("select");
        for (const select of selects) {
            for (const option of select.options) {
                if (option.selected === option.defaultSelected) continue;
                return true;
            }
        }
        return false;
    }

    confirmClose() {
        // if (this.isAnyFieldChanged()) {
        //     return confirm("You have unsaved changes.");
        // }
        return true;
    }

    closeWithoutSaving() {
        if (!this.confirmClose()) {
            return;
        }
        this.form.reset();
        return super.closeWithoutSaving();
    }
}

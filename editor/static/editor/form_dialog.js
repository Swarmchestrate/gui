import { Dialog } from "/static/dialog.js";
import { AsyncFormHandler } from "/static/editor/async_forms.js";

export class FormDialog extends Dialog {
    constructor(dialog, closeButtons, showButtons, options, form) {
        super(dialog, closeButtons, showButtons, options);
        if (!("onFormSuccess" in this.options)) {
            this.options.onFormSuccess = () => {};
        }
        this.onFormSuccess = this.options.onFormSuccess;
        this.asyncFormHandler = new AsyncFormHandler(form, {
            onSuccess: (responseData) => {
                this.onFormSuccess(responseData);
                this.close();
            },
        });
    }
}

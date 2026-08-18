import { EditorValidator } from "/static/editor/validation.js";
import { loadOneToOneFieldPopupSections } from "/static/editor/one_to_one_field_popup_sections.js";
import { loadOneToManyFieldPopupSections } from "/static/editor/one_to_many_field_popup_sections.js";
import { setupTextArrayFields } from "/static/editor/text_array_fields.js";
import { setupNodeFilterFields } from "/static/editor/node_filter_fields.js";

window.addEventListener("DOMContentLoaded", async () => {
    const form = document.querySelector("#fk-resource-form");
    const validator = new EditorValidator(form);
    validator.setupInlineValidation();
    loadOneToOneFieldPopupSections();
    // Awaited: the dialogs it injects are what the field setup below acts on.
    await loadOneToManyFieldPopupSections();
    setupNodeFilterFields();
    // Without this the list-valued fields render but have no listeners, so
    // typing never reaches the hidden input the form actually submits.
    setupTextArrayFields();
    const tooltipTriggerElements = Array.from(
        document.querySelectorAll("[data-bs-toggle='tooltip']"),
    );
    tooltipTriggerElements.forEach((tooltipTriggerElement) => {
        new bootstrap.Tooltip(tooltipTriggerElement);
    });
});
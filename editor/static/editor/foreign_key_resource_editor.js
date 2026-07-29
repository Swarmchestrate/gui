import { EditorValidator } from "/static/editor/validation.js";
import { loadOneToOneFieldSections } from "/static/editor/one_to_one_field_sections.js";
import { loadOneToManyFieldSections } from "/static/editor/one_to_many_field_sections.js";
import { setupTextArrayFields } from "/static/editor/text_array_fields.js";
import { setupNodeFilterFields } from "/static/editor/node_filter_fields.js";

window.addEventListener("DOMContentLoaded", async () => {
    const form = document.querySelector("#fk-resource-form");
    const validator = new EditorValidator(form);
    validator.setupInlineValidation();
    loadOneToOneFieldSections();
    // Awaited: the dialogs it injects are what the field setup below acts on.
    await loadOneToManyFieldSections();
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
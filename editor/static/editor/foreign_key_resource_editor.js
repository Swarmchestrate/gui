import { EditorValidator } from "/static/editor/validation.js";
import { loadOneToOneFieldSections } from "/static/editor/one_to_one_field_sections.js";
import { loadOneToManyFieldSections } from "/static/editor/one_to_many_field_sections.js";

window.addEventListener("DOMContentLoaded", async () => {
    const form = document.querySelector("#fk-resource-form");
    const validator = new EditorValidator(form);
    validator.setupInlineValidation();
    loadOneToOneFieldSections();
    loadOneToManyFieldSections();
    const tooltipTriggerElements = Array.from(
        document.querySelectorAll("[data-bs-toggle='tooltip']"),
    );
    tooltipTriggerElements.forEach((tooltipTriggerElement) => {
        new bootstrap.Tooltip(tooltipTriggerElement);
    });
});
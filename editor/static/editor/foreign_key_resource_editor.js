import { loadOneToOneFieldSections } from "/static/editor/editor_one_to_one_field_sections.js";
import { loadOneToManyFieldSections } from "/static/editor/editor_one_to_many_field_sections.js";

window.addEventListener("DOMContentLoaded", async () => {
    loadOneToOneFieldSections();
    loadOneToManyFieldSections();
    const tooltipTriggerElements = Array.from(
        document.querySelectorAll("[data-bs-toggle='tooltip']"),
    );
    tooltipTriggerElements.forEach((tooltipTriggerElement) => {
        new bootstrap.Tooltip(tooltipTriggerElement);
    });
});
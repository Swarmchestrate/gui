import { AsyncFormHandler } from "/static/editor/autosave.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";
import { loadOneToOneFieldPopupSections } from "/static/editor/one_to_one_field_popup_sections.js";
import { loadOneToManyFieldPopupSections } from "/static/editor/one_to_many_field_popup_sections.js";
import { loadOneToOneFieldSections } from "/static/editor/one_to_one_field_sections.js";
import { loadOneToManyFieldSections } from "/static/editor/one_to_many_field_sections.js";
import { setupTextArrayFields } from "/static/editor/text_array_fields.js";
import { displayToast } from "/static/editor/toasts.js";

function linkEditorTabSwitchingToCurrentPageCategory() {
    const tabPaneButtons = Array.from(
        document.querySelectorAll(".editor-toc button[data-bs-toggle='tab']"),
    );
    tabPaneButtons.forEach((tabPaneButton) => {
        tabPaneButton.addEventListener("shown.bs.tab", (event) => {
            const selectedTabPaneButton = event.target;
            const updatedCurrentCategory =
                selectedTabPaneButton.dataset.category;
            if ("URLSearchParams" in window) {
                const url = new URL(window.location);
                url.searchParams.set("category", updatedCurrentCategory);
                history.pushState(null, "", url);
            }
        });
    });
}

window.addEventListener("DOMContentLoaded", async () => {
    const bsEditorTab = new bootstrap.Tab("#editor-tab");
    linkEditorTabSwitchingToCurrentPageCategory();
    setupFormsetTables();
    loadOneToOneFieldPopupSections();
    loadOneToManyFieldPopupSections();
    loadOneToOneFieldSections();
    loadOneToManyFieldSections();
    setupTextArrayFields();
    const tooltipTriggerElements = Array.from(
        document.querySelectorAll("[data-bs-toggle='tooltip']"),
    );
    tooltipTriggerElements.forEach((tooltipTriggerElement) => {
        new bootstrap.Tooltip(tooltipTriggerElement);
    });
    // Implement autosave last to ensure any final preparations are
    // complete before form data is sent to the server (e.g., when
    // text array fields are exported as JSON to hidden inputs).
    const editorTabForms = Array.from(
        document.querySelectorAll("#editor-tab-content form"),
    );
    editorTabForms.forEach((form) => {
        const prevTabButton = form.querySelector("button[data-prev-tab-id]");
        if (prevTabButton) {
            const prevTabId = prevTabButton.dataset.prevTabId;
            const prevTab = document.querySelector(`#${prevTabId}`);
            const prevTabInstance = bootstrap.Tab.getOrCreateInstance(prevTab);
            prevTabButton.addEventListener("click", () => {
                prevTabInstance.show();
            });
        }
        const nextTabButton = form.querySelector("button[data-next-tab-id]");
        let nextTabInstance;
        if (nextTabButton) {
            const nextTabId = nextTabButton.dataset.nextTabId;
            const nextTab = document.querySelector(`#${nextTabId}`);
            nextTabInstance = bootstrap.Tab.getOrCreateInstance(nextTab);
            nextTabButton.addEventListener("click", () => {
                nextTabInstance.show();
            });
        }
        new AsyncFormHandler(form);
    });
});

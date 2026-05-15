import { AsyncFormHandler } from "/static/editor/async_forms.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";
import { loadOneToOneFields } from "/static/editor/one_to_one_field_loader.js";
import { loadOneToManyFields } from "/static/editor/one_to_many_field_loader.js";
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
        const asyncFormHandler = new AsyncFormHandler(form, {
            onSuccess: (responseData) => {
                const responseMessage =
                    responseData.message || "Applied changes.";
                displayToast(responseMessage);
            },
            statusButtonSelector: "button[type='submit']:not([form])",
        });
        asyncFormHandler.setup();
    });
    linkEditorTabSwitchingToCurrentPageCategory();
    setupFormsetTables();
    loadOneToOneFields();
    loadOneToManyFields();
    const tooltipTriggerElements = Array.from(
        document.querySelectorAll("[data-bs-toggle='tooltip']"),
    );
    tooltipTriggerElements.forEach((tooltipTriggerElement) => {
        new bootstrap.Tooltip(tooltipTriggerElement);
    });
});

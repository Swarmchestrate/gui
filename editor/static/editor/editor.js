import { AsyncFormHandler } from "/static/editor/async_forms.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";
import { getEditorTabbedFormHtml } from "/static/editor/editor_tabbed_form.js";
import { getEditorTocHtml } from "/static/editor/editor_toc.js";
import { initialiseOneToOneFields } from "/static/editor/one_to_one_fields.js";
import { initialiseOneToManyFields } from "/static/editor/one_to_many_fields.js";
import {
    displayToast,
    displayToastUntilDismissed,
} from "/static/editor/toasts.js";

const editorTocWrapper = document.querySelector(".editor-layout__toc");
const editorTabbedFormWrapper = document.querySelector(".editor-layout__body");

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
    const editorHtmlSections = await Promise.all([
        getEditorTabbedFormHtml(),
        getEditorTocHtml(),
    ]);
    const editorTocHtml = editorHtmlSections[1];
    editorTocWrapper.innerHTML = editorTocHtml;
    const editorTabbedFormHtml = editorHtmlSections[0];
    editorTabbedFormWrapper.innerHTML = editorTabbedFormHtml;
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
        new AsyncFormHandler(form, {
            onSuccess: (responseData) => {
                const responseMessage =
                    responseData.message || "Applied changes.";
                displayToast(responseMessage);
            },
        });
    });
    linkEditorTabSwitchingToCurrentPageCategory();
    setupFormsetTables();
    initialiseOneToOneFields();
    initialiseOneToManyFields();
});

import { AsyncFormHandler } from "/static/editor/async_forms.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";
import { loadEditorTabbedForm } from "/static/editor/editor_tabbed_form.js";
import { loadEditorToc } from "/static/editor/editor_toc.js";
import { initialiseOneToOneFields } from "/static/editor/one_to_one_fields.js";
import { initialiseOneToManyFields } from "/static/editor/one_to_many_fields.js";

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
    await Promise.all([loadEditorTabbedForm(), loadEditorToc()]);
    const editorTabForms = Array.from(
        document.querySelectorAll("#editor-tab-content form"),
    );
    editorTabForms.forEach((form) => {
        new AsyncFormHandler(form);
    });
    linkEditorTabSwitchingToCurrentPageCategory();
    setupFormsetTables();
    initialiseOneToOneFields();
    initialiseOneToManyFields();
});

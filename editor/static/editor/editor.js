import { AsyncFormHandler } from "/static/editor/async_forms.js";
import { setupFormsetTables } from "/static/editor/formset_tables.js";
import { loadEditorTabbedForm } from "/static/editor/editor_tabbed_form.js";
import { loadEditorToc } from "/static/editor/editor_toc.js";

window.addEventListener("DOMContentLoaded", async () => {
    await Promise.all([loadEditorTabbedForm(), loadEditorToc()]);
    const editorTabForms = Array.from(
        document.querySelectorAll("#editor-tab-content form"),
    );
    editorTabForms.forEach((form) => {
        new AsyncFormHandler(form);
    });
    setupFormsetTables();
});

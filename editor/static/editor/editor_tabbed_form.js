const editorTabbedFormUrl = JSON.parse(
    document.querySelector("#tabbed_form_url").textContent,
);
const editorTabbedFormWrapper = document.querySelector(".editor-layout__body");
const initialCategory = JSON.parse(
    document.querySelector("#initial_category").textContent,
);

export async function loadEditorTabbedForm() {
    const response = await fetch(
        `${editorTabbedFormUrl}?${new URLSearchParams({ category: initialCategory }).toString()}`,
        { method: "GET" },
    );
    if (!response.ok) {
        return console.error(
            "Could not load editor form due to an error: ",
            error,
        );
    }
    let responseContent = "";
    try {
        responseContent = await response.text();
    } catch (error) {
        return console.error(
            "Could not load editor form due to an error: ",
            error,
        );
    }
    editorTabbedFormWrapper.innerHTML = responseContent;
}

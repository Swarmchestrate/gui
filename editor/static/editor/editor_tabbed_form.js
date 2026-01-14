const editorTabbedFormUrl = JSON.parse(
    document.querySelector("#tabbed_form_url").textContent,
);
const initialCategory = JSON.parse(
    document.querySelector("#initial_category").textContent,
);

export async function getEditorTabbedFormHtml() {
    const response = await fetch(
        `${editorTabbedFormUrl}?${new URLSearchParams({ category: initialCategory }).toString()}`,
        { method: "GET" },
    );
    if (!response.ok) {
        console.error(
            "Received an error whilst loading the form: ",
            response.status,
            response.statusText,
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
    return responseContent;
}

const editorTabbedFormUrl = JSON.parse(
    document.querySelector("#tabbed_form_url").textContent,
);
const editorTabbedFormWrapper = document.querySelector(".editor-layout__body");

window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch(editorTabbedFormUrl, { method: "GET" });
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
});

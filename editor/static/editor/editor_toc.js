const editorTocUrl = JSON.parse(document.querySelector("#toc_url").textContent);
const editorTocWrapper = document.querySelector(".editor-layout__toc");

window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch(editorTocUrl, { method: "GET" });
    if (!response.ok) {
        return console.error(
            "Could not load editor table of contents due to an error: ",
            error,
        );
    }
    let responseContent = "";
    try {
        responseContent = await response.text();
    } catch (error) {
        return console.error(
            "Could not load editor table of contents due to an error: ",
            error,
        );
    }
    editorTocWrapper.innerHTML = responseContent;
});

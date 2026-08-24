import { htmlToNode } from "/static/editor/utils.js";

async function getSubsection(subsectionUrl) {
    const response = await fetch(subsectionUrl, {
        method: "GET",
    });
    if (!response.ok) {
        return console.error("Received an error trying to load a subsection.");
    }
    let responseContent = "";

    // Inspect text from the response, in
    // case something has gone wrong.
    try {
        responseContent = await response.text();
    } catch (error) {
        return console.error("Could not extract text from the response.");
    }
    
    return responseContent;
}

function replaceSubsectionPlaceholderWithError(subsectionPlaceholder) {
    const loadingErrorElement = document.createElement("span");
    loadingErrorElement.classList.add("text-danger");
    loadingErrorElement.textContent = "Could not load data for this field.";
    return subsectionPlaceholder.replaceWith(loadingErrorElement);
}

async function loadSubsections() {
    const subsectionPlaceholders = Array.from(
        document.querySelectorAll("[data-subsection-url]")
    );
    const subsectionUrls = subsectionPlaceholders.map(
        subsectionPlaceholder => subsectionPlaceholder.dataset.subsectionUrl
    );
    const subsectionHtmls = await Promise.all(subsectionUrls.map(subsectionUrl => getSubsection(subsectionUrl)));
    subsectionPlaceholders.forEach((subsectionPlaceholder, i) => {
        let subsection;
        try {
            subsection = htmlToNode(subsectionHtmls[i].trim());
        } catch (error) {
            return replaceSubsectionPlaceholderWithError(subsectionPlaceholder);
        }
        if (!subsection) {
            return replaceSubsectionPlaceholderWithError(subsectionPlaceholder);
        }
        subsectionPlaceholder.replaceWith(subsection);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadSubsections();
});
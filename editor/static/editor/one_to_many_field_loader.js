import { displayToast } from "/static/editor/toasts.js";
import { htmlToNode } from "/static/editor/utils.js";

async function getFieldContent(fieldContentUrl) {
    const response = await fetch(
        fieldContentUrl,
        { method: "GET" },
    );
    if (!response.ok) {
        console.error(
            "Received an error whilst loading field content: ",
            response.status,
            response.statusText,
        );
    }
    let responseContent = "";
    
    // Try to extract JSON from response, first.
    let isJsonInResponse = true;
    try {
        responseContent = await response.json();
    } catch (error) {
        isJsonInResponse = false;
        console.log("response", response);
        console.error("The response was not in the expected format.");
    }

    if (isJsonInResponse) {
        return responseContent;
    }

    // Inspect text from the response, in
    // case something has gone wrong.
    try {
        const content = await response.text();
        console.log("content", content);
    } catch (error) {
        console.error("Could not extract text from the response.");
    }
    return console.error(
        "Could not load field content due to an error."
    );
}

export async function loadOneToManyFields() {
    const oneToManyFields = Array.from(
        document.querySelectorAll(".one-to-many-field"),
    );
    const fieldContentUrls = oneToManyFields.map(field => field.querySelector("[data-content-url]").dataset.contentUrl);
    const htmlForFieldContents = await Promise.all(fieldContentUrls.map(fieldContentUrl => getFieldContent(fieldContentUrl)));
    oneToManyFields.forEach((field, i) => {
        const fieldContentPlaceholder = field.querySelector("[data-content-url]");
        const fieldContent = htmlToNode(htmlForFieldContents[i].initial_content.trim());
        fieldContentPlaceholder.replaceWith(fieldContent);
        fieldContent.append(htmlToNode(htmlForFieldContents[i].new_editor.trim()));
        const templatesForResources = htmlForFieldContents[i].existing_resource_templates;
        for (const resourceId in templatesForResources) {
            const templatesForResource = templatesForResources[resourceId];
            fieldContent.append(htmlToNode(templatesForResource.update_editor.trim()));
            fieldContent.append(htmlToNode(templatesForResource.delete_dialog.trim()));
        }
        const headElement = document.querySelector("head");
        const templates = htmlForFieldContents[i].templates;
        headElement.append(htmlToNode(templates.update_editor.trim()));
        headElement.append(htmlToNode(templates.delete_dialog.trim()));
        headElement.append(htmlToNode(templates.list_item.trim()));
        // new OneToManyField(field);
    });
}
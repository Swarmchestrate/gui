export function htmlToNode(html) {
    // Credit: https://stackoverflow.com/a/35385518/10640126
    const template = document.createElement("TEMPLATE");
    template.innerHTML = html;
    const numNodes = template.content.childNodes.length;
    if (numNodes !== 1) {
        throw new Error(`html parameter must represent a single node; got ${numNodes} nodes.
            Note that leading or trailing spaces around an element in your HTML, like
            "</img> ", get parsed as text nodes neighbouring the element; call .trim() on
            your input to avoid this.
        `);
    }
    return template.content.firstChild;
}

export function updateElementPlaceholderAttributes(element, formsetIndex) {
    const formsetTemplateElements = element.querySelectorAll(
        '[id*="__prefix__"], [for*="__prefix__"], [name*="__prefix__"]',
    );
    for (const element of formsetTemplateElements) {
        for (const attribute of element.attributes) {
            if (!attribute.value.includes("__prefix__")) {
                continue;
            }
            element.setAttribute(
                attribute.name,
                attribute.value.replace("__prefix__", formsetIndex),
            );
        }
    }
    return element;
}

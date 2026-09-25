// Validating asks SAT Builder to build the template, which takes a moment. Show
// that it is working, and stop a second click sending it again.
document.addEventListener("submit", (event) => {
    if (!event.target.matches(".validate-form")) {
        return;
    }
    const button = event.submitter;
    if (!button) {
        return;
    }
    button.disabled = true;
    const spinner = document.createElement("span");
    spinner.classList.add("spinner-border", "spinner-border-sm");
    spinner.setAttribute("aria-hidden", "true");
    button.replaceChildren(spinner);
    const label = document.createElement("span");
    if (button.dataset.busyText) {
        label.textContent = ` ${button.dataset.busyText}`;
    } else {
        label.classList.add("visually-hidden");
        label.textContent = "Validating";
    }
    button.append(label);
});

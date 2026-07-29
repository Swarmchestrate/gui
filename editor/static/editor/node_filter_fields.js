/**
 * Narrows a resource requirement's comparison to the target it is written
 * against.
 *
 * A form field's choices are fixed when the field is built, so the operator
 * select carries every operator. Which of them mean anything depends on the
 * target: a range over a string matches nothing, and the profile knows it. This
 * asks the server for that map once and applies it as the target changes, so
 * an impossible requirement cannot be built rather than being refused later.
 */
const OPERATORS_URL = "/applications/api/node-filter/operators/";
const RANGE_OPERATOR = "$in_range";

class NodeFilterFields {
    constructor(form, operatorsByTarget) {
        this.targetSelect = form.querySelector("select[name='target']");
        this.operatorSelect = form.querySelector("select[name='operator']");
        this.operatorsByTarget = operatorsByTarget;
        // Kept so options can be restored when the target changes again.
        this.allOperatorOptions = Array.from(this.operatorSelect.options).map(
            (option) => ({ value: option.value, text: option.text }),
        );
        this.upperBoundField = this.fieldWrapperFor(form, "value_max");

        this.targetSelect.addEventListener("change", () => this.apply());
        this.operatorSelect.addEventListener("change", () => this.showUpperBound());
        this.apply();
    }

    fieldWrapperFor(form, name) {
        const input = form.querySelector(`[name='${name}']`);
        return input ? input.closest("div.py-4") || input.parentElement : null;
    }

    apply() {
        const allowed = this.operatorsByTarget[this.targetSelect.value];
        const chosen = this.operatorSelect.value;

        this.operatorSelect.replaceChildren();
        for (const option of this.allOperatorOptions) {
            // An unknown target leaves every operator available rather than
            // emptying the list and blocking the form.
            if (option.value && allowed && !allowed.includes(option.value)) {
                continue;
            }
            const element = document.createElement("option");
            element.value = option.value;
            element.text = option.text;
            this.operatorSelect.append(element);
        }

        // Keep the operator if it still applies; otherwise fall back to the
        // first one, so the field is never left showing something invalid.
        const stillValid = Array.from(this.operatorSelect.options).some(
            (option) => option.value === chosen,
        );
        this.operatorSelect.value = stillValid ? chosen : this.operatorSelect.options[0].value;
        this.showUpperBound();
    }

    showUpperBound() {
        if (!this.upperBoundField) {
            return;
        }
        const isRange = this.operatorSelect.value === RANGE_OPERATOR;
        this.upperBoundField.classList.toggle("d-none", !isRange);
    }
}

export async function setupNodeFilterFields(root = document) {
    const forms = Array.from(root.querySelectorAll("form")).filter(
        (form) =>
            form.querySelector("select[name='target']") &&
            form.querySelector("select[name='operator']"),
    );
    if (!forms.length) {
        return;
    }

    let operatorsByTarget;
    try {
        const response = await fetch(OPERATORS_URL, {
            headers: { Accept: "application/json" },
        });
        if (!response.ok) {
            return;
        }
        ({ operatorsByTarget } = await response.json());
    } catch (error) {
        // Leaving every operator on offer is worse than narrowing them, but far
        // better than a form that will not render.
        console.error(error);
        return;
    }

    for (const form of forms) {
        new NodeFilterFields(form, operatorsByTarget);
    }
}

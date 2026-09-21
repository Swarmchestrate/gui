import json

from django import forms
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class SelectWithDisabledFirstOption(forms.Select):
    # Implementation adapted from: https://stackoverflow.com/a/54012408
    DISABLED_OPTION_INDEX = 0

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if option["index"] == self.DISABLED_OPTION_INDEX:
            option["attrs"]["disabled"] = ""
        return option


class GeometryPointWidget(forms.MultiWidget):
    template_name = "editor/widgets/geometry_point_widget.html"

    def decompress(self, value):
        if value:
            return [value.get("latitude"), value.get("longitude")]
        return [None, None]


class KeyValueWidget(forms.Widget):
    """Edits a flat name/value map as rows, rather than as JSON typed by hand.

    The map travels in a hidden input as JSON, which is what the form field
    parses; the visible rows are kept in step with it by key_value_fields.js.
    The script listens at the document, so rows work in dialogs injected after
    the page loads without anything having to set them up.
    """

    has_feedback_element = True
    ROW = (
        '<li class="list-group-item key-value-row"><div class="d-flex gap-2">'
        '<input type="text" class="form-control" data-kv="key" placeholder="Name" value="{}" aria-label="Name">'
        '<input type="text" class="form-control" data-kv="value" placeholder="Value" value="{}" aria-label="Value">'
        '<button type="button" class="btn btn-outline-danger delete-btn" aria-label="Delete" title="Delete">'
        '<i class="bi bi-trash3-fill"></i></button></div></li>'
    )

    def _as_map(self, value) -> dict:
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value.strip():
            try:
                parsed = json.loads(value)
            except ValueError:
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}

    def render(self, name, value, attrs=None, renderer=None):
        mapping = self._as_map(value)
        field_id = (attrs or {}).get("id") or f"id_{name}"
        rows = format_html_join("", self.ROW, ((k, v) for k, v in mapping.items()))
        return format_html(
            '<div class="key-value-field card w-100" data-field-id="{}">'
            '<ul class="list-group list-group-flush">{}</ul>'
            '<template>{}</template>'
            '<button type="button" class="btn btn-light add-btn rounded-top-0 w-100">'
            '<i class="bi bi-plus-lg"></i> Add</button>'
            '<input type="hidden" name="{}" id="{}" value="{}">'
            '{}'
            '</div>',
            field_id,
            rows,
            format_html(self.ROW, "", ""),
            name,
            field_id,
            json.dumps(mapping),
            render_to_string(
                "editor/field_templates/invalid_feedback.html",
                {"invalid_feedback_id_prefix": field_id}
            )
        )

    def value_from_datadict(self, data, files, name):
        return data.get(name)


class CheckboxListWidget(forms.CheckboxSelectMultiple):
    """Checkboxes laid out the way Bootstrap expects.

    Django's own markup puts each input inside its label with no .form-check
    wrapper, and Bootstrap's negative margin on .form-check-input then pulls the
    box outside its container and over the neighbouring text.
    """

    # Not "checkbox": templates send that to the single-checkbox layout, which
    # puts the label after the box. A list wants its label above, like any field.
    input_type = "checkbox-list"

    def render(self, name, value, attrs=None, renderer=None):
        if value in (None, ""):
            selected = set()
        elif isinstance(value, (list, tuple)):
            selected = {str(v) for v in value}
        else:
            selected = {str(value)}
        base_id = (attrs or {}).get("id") or f"id_{name}"
        options = format_html_join(
            "",
            '<div class="form-check"><input class="form-check-input" type="checkbox" '
            'name="{}" value="{}" id="{}_{}"{}><label class="form-check-label" '
            'for="{}_{}">{}</label></div>',
            (
                (name, option_value, base_id, index,
                 mark_safe(" checked") if str(option_value) in selected else "",
                 base_id, index, label)
                for index, (option_value, label) in enumerate(self.choices)
            ),
        )
        return format_html('<div id="{}" class="d-flex flex-column gap-1">{}</div>', base_id, options)

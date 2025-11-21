from django.forms import CheckboxInput

from editor.base_formsets import BaseEditorFormSet


class InstanceTypeFormSet(BaseEditorFormSet):
    non_api_data_fields = [
        "DELETE",
        "unsaved",
    ]

    def to_api_ready_format(self):
        formatted_data = list()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            if not data:
                continue
            if data.get("DELETE") is True:
                continue
            for field in self.non_api_data_fields:
                data.pop(field, None)
            formatted_data.append(data)
        return formatted_data

    def get_deletion_widget(self):
        return CheckboxInput(
            attrs={
                "class": "form-check-input delete-list-item",
                "data-bs-title": "Delete",
                "data-bs-placement": "left",
            }
        )

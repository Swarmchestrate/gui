from django.forms import CheckboxInput

from editor.formsets import BaseEditorFormSet


class InstanceTypeFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = list()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            if not data:
                continue
            if data.get('DELETE') is True:
                continue
            data.pop('DELETE')
            formatted_data.append(data)
        return formatted_data

    def get_deletion_widget(self):
        return CheckboxInput(attrs={
            'class': 'btn-check',
        })

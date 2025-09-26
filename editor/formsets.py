from django.forms import BaseFormSet, CheckboxInput


class BaseEditorFormset(BaseFormSet):
    def get_deletion_widget(self):
        return CheckboxInput(attrs={
            'class': 'form-check-input',
        })

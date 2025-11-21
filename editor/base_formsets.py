from abc import ABC, abstractmethod

from django.forms import BaseFormSet, CheckboxInput, Form


class BaseEditorFormSet(ABC, BaseFormSet):
    def get_cleaned_data_from_form(self, form: Form):
        if (self.can_delete
            and self._should_delete_form(form)):
            return dict()
        return form.cleaned_data

    @abstractmethod
    def to_api_ready_format(self) -> dict | list:
        pass

    def get_deletion_widget(self):
        return CheckboxInput(attrs={
            'class': 'form-check-input',
        })

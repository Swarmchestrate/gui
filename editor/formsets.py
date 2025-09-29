from django.forms import BaseFormSet, CheckboxInput, Form


class BaseEditorFormset(BaseFormSet):
    def get_cleaned_data_from_form(self, form: Form):
        if (self.can_delete
            and self._should_delete_form(form)):
            return dict()
        return form.cleaned_data

    def to_api_ready_format(self):
        pass

    def get_deletion_widget(self):
        return CheckboxInput(attrs={
            'class': 'form-check-input',
        })

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
            formatted_data.append(data)
        return formatted_data

from editor.forms.formsets import BaseEditorFormSet


# Cloud Capacity formsets
class CloudCapacityArchitectureEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self) -> dict | list:
        formatted_data = list()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            architecture_name = data.get("architecture_name", "")
            if not architecture_name.strip():
                continue
            formatted_data.append(architecture_name)
        return formatted_data


class CloudCapacityOperatingSystemEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self) -> dict | list:
        formatted_data = dict()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            os_name = data.get("os_name", "")
            os_id = data.get("os_id", "")
            if not os_name.strip() or not os_id.strip():
                continue
            formatted_data.update(
                {
                    os_name: os_id,
                }
            )
        return formatted_data

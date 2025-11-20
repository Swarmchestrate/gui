from editor.forms.formsets import BaseEditorFormSet


# Edge Capacity formsets
class EdgeCapacityAccessibleSensorsEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = list()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            sensor_name = data.get("sensor_name", "")
            if not sensor_name.strip():
                continue
            formatted_data.append(sensor_name)
        return formatted_data


class EdgeCapacityDevicesEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = dict()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            if not data:
                continue
            device_type = data.get("device_type")
            device_name = data.get("device_name")
            formatted_data.update(
                {
                    device_type: device_name,
                }
            )
        return formatted_data

from editor.base_formsets import BaseEditorFormSet


# Cloud & Edge Capacity formsets
class CapacityPriceEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = dict()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            if not data:
                continue
            formatted_data.update(
                {
                    data.get("instance_type"): "%s credit/hour"
                    % (data.get("credits_per_hour"))
                }
            )
        return formatted_data


class CapacityEnergyConsumptionEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = dict()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            if not data:
                continue
            formatted_data.update(
                {
                    data.get("type"): data.get("amount"),
                }
            )
        return formatted_data


class CapacitySecurityPortsEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self):
        formatted_data = list()
        for form in self:
            data = self.get_cleaned_data_from_form(form)
            port_number = str(data.get("port_number", ""))
            if not port_number.strip():
                continue
            formatted_data.append(port_number)
        return formatted_data

from editor.forms.formsets import BaseEditorFormSet


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


class CapacityLocalityEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self) -> dict | list:
        formatted_data = dict()
        form = next(iter(self))
        data = self.get_cleaned_data_from_form(form)
        # Continent
        continent = data.get("continent")
        if not continent:
            return formatted_data
        formatted_data.update(
            {
                "continent": continent,
            }
        )
        # Country
        country = data.get("country")
        if not country:
            return formatted_data
        formatted_data.update(
            {
                "country": country,
            }
        )
        # City
        city = data.get("city")
        if not city:
            return formatted_data
        formatted_data.update(
            {
                "city": city,
            }
        )
        # GPS
        gps = data.get("gps")
        if not gps:
            return formatted_data
        formatted_data.update(
            {
                "gps": gps,
            }
        )
        return formatted_data

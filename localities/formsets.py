from editor.base_formsets import BaseEditorFormSet


class LocalityEditorFormSet(BaseEditorFormSet):
    def to_api_ready_format(self) -> dict | list:
        formatted_data = dict()
        form = next(iter(self), None)
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

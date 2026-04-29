from django import forms


class SelectWithDisabledFirstOption(forms.Select):
    # Implementation adapted from: https://stackoverflow.com/a/54012408
    DISABLED_OPTION_INDEX = 0

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if option["index"] == self.DISABLED_OPTION_INDEX:
            option["attrs"]["disabled"] = ""
        return option


class GeometryPointWidget(forms.MultiWidget):
    template_name = "editor/widgets/geometry_point_widget.html"

    def decompress(self, value):
        if value:
            return [value.get("latitude"), value.get("longitude")]
        return [None, None]

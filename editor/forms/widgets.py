from django import forms


class SelectWithDisabledFirstOption(forms.Select):
    # Implementation adapted from: https://stackoverflow.com/a/54012408
    DISABLED_OPTION_INDEX = 0

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if option["index"] == self.DISABLED_OPTION_INDEX:
            option["attrs"]["disabled"] = ""
        return option

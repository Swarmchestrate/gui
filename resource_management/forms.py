from django import forms


class ResourceDeletionForm(forms.Form):
    def __init__(self, resource_ids: list[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resource_ids_to_delete"].choices = [
            (id, id) for id in resource_ids
        ]

    resource_ids_to_delete = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
                "aria-label": "Select",
            }
        ),
    )

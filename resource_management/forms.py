from django import forms

from editor.forms.base_forms import OpenApiSpecificationBasedForm


class OpenApiSpecificationBasedFormWithSuffix(OpenApiSpecificationBasedForm):
    def __init__(self, *args, id_suffix: str = "", **kwargs):
        kwargs.update({"auto_id": f"id_%s_{id_suffix}"})
        super().__init__(*args, **kwargs)


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
                "aria-label": "Select row",
            }
        ),
    )

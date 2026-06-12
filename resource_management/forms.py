from django import forms

from editor.forms import FormWithDynamicallyPopulatedFields
from postgrest.table_names import PostGisTableNames


class FormWithIdAttributeSuffix(forms.Form):
    def __init__(self, *args, id_suffix: str = "", **kwargs):
        kwargs.update({"auto_id": f"id_%s_{id_suffix}"})
        super().__init__(*args, **kwargs)


class ResourceDeletionForm(FormWithIdAttributeSuffix):
    resource_id_to_delete = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )


class MultiResourceDeletionForm(forms.Form):
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


# Column Metadata
class NewColumnMetadataEditorForm(FormWithDynamicallyPopulatedFields):
    def __init__(self, *args, table_names: list[str] = None, fields = None, **kwargs):
        if "table_name" not in fields:
            return super().__init__(*args, fields=fields, **kwargs)
        if not table_names:
            table_names = list()
        fields.update({
            "table_name": self.get_choice_based_table_name_field(
                fields.get("table_name"),
                table_names
            ),
            "column_name": self.get_column_name_field(
                fields.get("table_name")
            ),
        })
        super().__init__(*args, fields=fields, **kwargs)

    def get_choice_based_table_name_field(
            self,
            original_table_name_field: forms.Field,
            table_names: list[str]):
        label_original = original_table_name_field.label
        required_original = original_table_name_field.required
        return forms.ChoiceField(
            label=label_original,
            required=required_original,
            choices=[
                ("", ""),
                *sorted([
                    (table_name, table_name)
                    for table_name in table_names
                    if table_name not in PostGisTableNames
                ])
            ],
            widget=forms.Select(attrs={
                "class": "form-select",
            })
        )

    def get_column_name_field(
            self,
            original_column_name_field: forms.Field,):
        label_original = original_column_name_field.label
        required_original = original_column_name_field.required
        return forms.CharField(
            label=label_original,
            required=required_original,
            widget=forms.Select(
                choices=[("", "")],
                attrs={
                    "disabled": "",
                    "class": "form-select",
                }
            )
        )



class ColumnMetadataDeletionForm(FormWithIdAttributeSuffix):
    resource_id_to_delete = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )

from enum import Enum

from django import forms

from editor.api.endpoints.base import (
    ApiEndpoint,
    ColumnMetadataApiEndpoint,
)


class OpenApiPropertyFormat(Enum):
    BOOLEAN = "boolean"
    CHARACTER_VARYING = "character varying"
    DATE = "timestamp without time zone"
    DOUBLE_PRECISION = "double precision"
    INTEGER = "integer"
    JSONB = "jsonb"
    NUMERIC = "numeric"
    TEXT = "text"
    TEXT_ARRAY = "text[]"


class EditorForm(forms.Form):
    error_css_class = "is-invalid"

    def is_valid(self):
        result = super().is_valid()
        fields_with_errors = self.errors
        if "__all__" in self.errors:
            fields_with_errors = self.fields
        for field_name in fields_with_errors:
            attrs = self.fields[field_name].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
        return result


class OpenApiSpecificationBasedForm(EditorForm):
    error_css_class = "is-invalid"
    definition_name = ""

    def __init__(
        self,
        api_endpoint: ApiEndpoint,
        column_metadata_api_endpoint: ColumnMetadataApiEndpoint,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.api_endpoint = api_endpoint
        self.column_metadata_api_endpoint = column_metadata_api_endpoint
        self.required_field_names = (
            self.api_endpoint.endpoint_definition.get_required_field_names()
        )
        field_data = self.get_data_for_form_fields()
        self.populate_form_fields(field_data)

    def is_valid(self):
        is_valid = super().is_valid()
        errors = self.errors.as_data()
        for field_name in errors:
            try:
                field = self.fields[field_name]
                f_classes = field.widget.attrs.get("class", "").split(" ")
                f_classes.append(self.error_css_class)
                field.widget.attrs.update(
                    {
                        "class": " ".join(f_classes),
                    }
                )
            except KeyError:
                continue
        return is_valid

    def get_data_for_form_fields(self):
        column_metadata = self.column_metadata_api_endpoint.get_registrations()
        field_data = (
            self.api_endpoint.endpoint_definition.get_all_user_specifiable_fields()
        )
        for cm in column_metadata:
            field_name = cm.get("column_name")
            try:
                field_data[field_name].update(cm)
            except KeyError:
                pass
        return field_data

    def populate_form_fields(self, field_data: dict):
        for field_key, field_metadata in field_data.items():
            is_required = field_key in self.required_field_names
            field = self.get_field(field_metadata, is_required=is_required)
            self.fields.update(
                {
                    field_key: field,
                }
            )

    def _get_initial_field_vars_from_field_format(self, field_format: str):
        field_class = forms.CharField
        widget_class = None
        css_classes: list = ["form-control"]
        format_enum = None
        try:
            format_enum = OpenApiPropertyFormat(field_format)
        except ValueError:
            pass
        match format_enum:
            case OpenApiPropertyFormat.BOOLEAN:
                field_class = forms.BooleanField
                css_classes = ["form-check-input"]
            case OpenApiPropertyFormat.DATE:
                field_class = forms.DateField
            case OpenApiPropertyFormat.INTEGER:
                field_class = forms.IntegerField
            case OpenApiPropertyFormat.NUMERIC | OpenApiPropertyFormat.DOUBLE_PRECISION:
                field_class = forms.FloatField
            case (
                OpenApiPropertyFormat.TEXT
                | OpenApiPropertyFormat.TEXT_ARRAY
                | OpenApiPropertyFormat.JSONB
            ):
                widget_class = forms.Textarea
        if not widget_class:
            widget_class = field_class.widget
        return {
            "field_class": field_class,
            "widget_class": widget_class,
            "css_classes": css_classes,
        }

    def _configure_field_kwargs(
        self,
        field_metadata: dict,
        widget_class,
        css_classes: list[str],
        is_required: bool,
    ):
        kwargs = {
            "required": is_required,
            "widget": widget_class(
                attrs={
                    "class": " ".join(css_classes),
                }
            ),
        }
        field_label = field_metadata.get("title")
        if field_label:
            kwargs.update(
                {
                    "label": field_label,
                }
            )
        field_description = field_metadata.get("description")
        if field_description:
            kwargs.update(
                {
                    "help_text": field_description,
                }
            )
            kwargs["widget"].attrs.update(
                {
                    "aria-describedby": f"{field_metadata.get('column_name')}-help-text",
                }
            )
        return kwargs

    def get_field(
        self, field_metadata: dict, is_required: bool = False
    ) -> list[forms.Field]:
        # Determine field, widget and/or widget CSS classes
        # from OpenAPI spec metadata.
        (
            field_class,
            widget_class,
            css_classes,
        ) = self._get_initial_field_vars_from_field_format(
            field_metadata.get("format", "")
        ).values()

        # Build field kwargs
        kwargs = self._configure_field_kwargs(
            field_metadata, widget_class, css_classes, is_required
        )

        return field_class(**kwargs)


class OpenApiSpecificationCategoryBasedForm(OpenApiSpecificationBasedForm):
    def __init__(self, api_endpoint: ApiEndpoint, category: str, *args, **kwargs):
        self.category = category
        super().__init__(api_endpoint, *args, **kwargs)

    def get_data_for_form_fields(self):
        column_metadata = self.column_metadata_api_endpoint.get_by_category(
            self.category
        )
        field_names = [r.get("column_name") for r in column_metadata]
        field_data = self.api_endpoint.endpoint_definition.get_user_specifiable_fields_with_names(
            field_names
        )
        for cm in column_metadata:
            field_name = cm.get("column_name")
            try:
                field_data[field_name].update(cm)
            except KeyError:
                pass
        return field_data


class OpenApiSpecificationBasedRegistrationForm(OpenApiSpecificationBasedForm):
    def get_data_for_form_fields(self):
        params = {
            "column_name": "in.(%s)"
            % (",".join([f'"{rfn}"' for rfn in self.required_field_names])),
        }
        column_metadata = self.column_metadata_api_endpoint.get_registrations(
            params=params
        )
        field_data = (
            self.api_endpoint.endpoint_definition.get_required_user_specifiable_fields()
        )
        for cm in column_metadata:
            field_name = cm.get("column_name")
            try:
                field_data[field_name].update(cm)
            except KeyError:
                pass
        return field_data


class RegistrationsListForm(forms.Form):
    def __init__(self, registration_ids: list[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["registration_ids_to_delete"].choices = [
            (id, id) for id in registration_ids
        ]

    registration_ids_to_delete = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
                "aria-label": "Select",
            }
        ),
    )


class LocalityEditorForm(EditorForm):
    continent = forms.CharField(
        label="Continent",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. Europe",
        required=False,
    )

    country = forms.CharField(
        label="Country",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. United Kingdom",
        required=False,
    )

    city = forms.CharField(
        label="City",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. London",
        required=False,
    )

    gps = forms.CharField(
        label="GPS Location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text="e.g. 51.5072, -0.1276",
        required=False,
    )

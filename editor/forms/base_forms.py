from enum import Enum

import lxml.html
from django import forms

from editor.api.base_api_clients import (
    ApiClient,
    ColumnMetadataApiClient,
)
from editor.api.mocks.mock_base_api_clients import MockApiClient


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
        api_client: ApiClient,
        column_metadata_api_client: ColumnMetadataApiClient,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.api_client = api_client
        self.column_metadata_api_client = column_metadata_api_client
        self.required_field_names = (
            self.api_client.endpoint_definition.get_required_field_names()
        )
        field_data = self.get_data_for_form_fields()
        field_data = self.add_extra_metadata_to_field_data(field_data)
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

    def add_extra_metadata_to_field_data(self, field_data: dict):
        column_metadata = self.column_metadata_api_client.get_resources()
        disabled_column_metadata = (
            self.column_metadata_api_client.get_resources_for_disabled_categories()
        )
        column_metadata.extend(disabled_column_metadata)
        column_metadata_by_column_name = dict(
            (cm.get("column_name"), cm) for cm in column_metadata
        )
        for field_name, field_metadata in field_data.items():
            cm = column_metadata_by_column_name.get(field_name)
            if not cm:
                continue
            cm.update({"help_text": cm.get("description")})
            cm.pop("description", None)
            field_name = cm.get("column_name")
            try:
                field_data[field_name].update(cm)
            except KeyError:
                pass
        return field_data

    def get_data_for_form_fields(self) -> dict:
        field_data = (
            self.api_client.endpoint_definition.get_all_user_specifiable_fields()
        )
        return field_data

    def populate_form_fields(self, field_data: dict):
        for field_key, field_metadata in field_data.items():
            is_required = field_key in self.required_field_names
            field = self.get_field(field_key, field_metadata, is_required=is_required)
            self.fields.update({field_key: field})

    def _get_initial_field_vars_from_field_format(self, field_format: str):
        field_class = forms.CharField
        widget_class = None
        css_classes: list = ["form-control"]
        format_enum = None
        extra_field_kwargs = dict()
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
                extra_field_kwargs.update({"min_value": 1, "step_size": 1})
            case OpenApiPropertyFormat.NUMERIC | OpenApiPropertyFormat.DOUBLE_PRECISION:
                field_class = forms.FloatField
                extra_field_kwargs.update({"min_value": 1, "step_size": "any"})
            case OpenApiPropertyFormat.TEXT_ARRAY | OpenApiPropertyFormat.JSONB:
                widget_class = forms.Textarea
        if not widget_class:
            widget_class = field_class.widget
        return {
            "field_class": field_class,
            "widget_class": widget_class,
            "css_classes": css_classes,
            "extra_field_kwargs": extra_field_kwargs,
        }

    def _configure_field_kwargs(
        self,
        field_metadata: dict,
        widget_class,
        css_classes: list[str],
        is_required: bool,
        extra_field_kwargs: dict | None = None,
    ):
        if not extra_field_kwargs:
            extra_field_kwargs = dict()
        kwargs = {
            "required": is_required,
            "widget": widget_class(attrs={"class": " ".join(css_classes)}),
        }
        field_label = field_metadata.get("title")
        if field_label:
            kwargs.update(
                {
                    "label": field_label,
                }
            )
        help_text = field_metadata.get("help_text")
        if help_text:
            kwargs.update(
                {
                    "help_text": help_text,
                }
            )
            kwargs["widget"].attrs.update(
                {
                    "aria-describedby": f"{field_metadata.get('column_name')}-help-text",
                }
            )
        kwargs.update(extra_field_kwargs)
        return kwargs

    def _get_field_components_for_foreign_key_referrer_field(
        self, field_metadata: dict
    ) -> dict | None:
        if not field_metadata.get("type") == "foreign_key_referrer":
            return
        endpoint = field_metadata.get("endpoint", "")
        fk_referrer_api_client = MockApiClient.get_client_instance_by_endpoint(endpoint)
        choices = []
        if fk_referrer_api_client:
            resources = fk_referrer_api_client.get_resources()
            choices = [
                (
                    r.get(fk_referrer_api_client.endpoint_definition.id_field),
                    f"{fk_referrer_api_client.endpoint.title()} {r.get(fk_referrer_api_client.endpoint_definition.id_field)}",
                )
                for r in resources
            ]
        field_class = forms.MultipleChoiceField
        return {
            "field_class": field_class,
            "widget_class": field_class.widget,
            "css_classes": ["form-select"],
            "extra_field_kwargs": {
                "choices": choices,
            },
        }

    def _get_field_components_for_foreign_key_field(
        self, field_name: str
    ) -> dict | None:
        definition = self.api_client.endpoint_definition
        field_metadata = definition.get_field(field_name)
        if not field_metadata.get("description"):
            return
        field_description = lxml.html.fromstring(field_metadata.get("description"))
        fk_table_name = next(iter(field_description.xpath("fk/@table")), None)

        # Get endpoint for the foreign key
        api_client = MockApiClient.get_client_instance_by_endpoint(fk_table_name)
        if not api_client:
            return
        # Get resources at endpoint
        resources = api_client.get_resources()
        # Return field components in a dict
        choices = (
            (
                r.get(api_client.endpoint_definition.id_field),
                f"{api_client.endpoint.title()} {r.get(api_client.endpoint_definition.id_field)}",
            )
            for r in resources
        )
        field_class = forms.ChoiceField
        return {
            "field_class": field_class,
            "widget_class": field_class.widget,
            "css_classes": ["form-select"],
            "extra_field_kwargs": {
                "choices": choices,
            },
        }

    def _get_field_components_for_enum_field(self, field_metadata: dict):
        format = field_metadata.get("format", "")
        if not format.endswith("enum"):
            return
        field_class = forms.ChoiceField
        field_enums = field_metadata.get("enum", [])
        if not field_enums:
            return
        choices = (
            (field_enum, field_enum.replace("_", " ")) for field_enum in field_enums
        )
        return {
            "field_class": field_class,
            "widget_class": field_class.widget,
            "css_classes": ["form-select"],
            "extra_field_kwargs": {
                "choices": choices,
            },
        }

    def get_field(
        self, field_name: str, field_metadata: dict, is_required: bool = False
    ) -> forms.Field:
        field_components = self._get_field_components_for_foreign_key_referrer_field(
            field_metadata
        )
        if not field_components:
            field_components = self._get_field_components_for_foreign_key_field(
                field_name
            )
        if not field_components:
            field_components = self._get_field_components_for_enum_field(field_metadata)
        if not field_components:
            # Determine field, widget and/or widget CSS classes
            # from OpenAPI spec metadata.
            field_components = self._get_initial_field_vars_from_field_format(
                field_metadata.get("format", "")
            )
        (
            field_class,
            widget_class,
            css_classes,
            extra_field_kwargs,
        ) = field_components.values()

        # Build field kwargs
        kwargs = self._configure_field_kwargs(
            field_metadata,
            widget_class,
            css_classes,
            is_required,
            extra_field_kwargs=extra_field_kwargs,
        )

        field = field_class(**kwargs)
        category = field_metadata.get("category")
        if not category:
            category = "Uncategorised"
        field.category = category
        return field


class OpenApiSpecificationCategoryBasedForm(OpenApiSpecificationBasedForm):
    def __init__(self, api_client: ApiClient, category: str, *args, **kwargs):
        self.category = category
        super().__init__(api_client, *args, **kwargs)

    def get_data_for_form_fields(self) -> dict:
        field_data = super().get_data_for_form_fields()
        if self.category.lower() == "uncategorised":
            column_metadata = self.column_metadata_api_client.get_resources()
            disabled_column_metadata = (
                self.column_metadata_api_client.get_resources_for_disabled_categories()
            )
            column_metadata.extend(disabled_column_metadata)
            column_names = set(
                cm.get("column_name", "")
                for cm in column_metadata
                if cm.get("category")
            )
            field_names = set(field_name for field_name in field_data.keys())
            uncategorised_field_names = field_names - column_names
            field_data = {
                field_name: field_value
                for field_name, field_value in field_data.items()
                if field_name in uncategorised_field_names
            }
            return field_data
        extra_metadata = self.column_metadata_api_client.get_resources_by_category(
            self.category
        )
        column_names = [em.get("column_name") for em in extra_metadata]
        field_data = {
            field_name: field_value
            for field_name, field_value in field_data.items()
            if field_name in column_names
        }
        return field_data


class OpenApiSpecificationBasedRegistrationForm(OpenApiSpecificationBasedForm):
    def get_data_for_form_fields(self) -> dict:
        field_data = super().get_data_for_form_fields()
        required_field_names = (
            self.api_client.endpoint_definition._get_required_field_names()
        )
        field_data = {
            field_name: field_value
            for field_name, field_value in field_data.items()
            if field_name in required_field_names
        }
        return field_data

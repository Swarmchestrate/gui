from enum import Enum

from django import forms

from postgrest.api_clients import ColumnMetadataApiClient

# from postgrest.base.base_api_clients import ApiClient
from postgrest.mocks.base.mock_base_api_clients import MockApiClient as ApiClient
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY

from .custom_fields import EnumField, GeometryPointField
from .custom_widgets import GeometryPointWidget, SelectWithDisabledFirstOption


class OpenApiPropertyFormat(Enum):
    BOOLEAN = "boolean"
    CHARACTER_VARYING = "character varying"
    DATE = "timestamp without time zone"
    DOUBLE_PRECISION = "double precision"
    GEOMETRY = "public.geometry"
    INTEGER = "integer"
    JSONB = "jsonb"
    NUMERIC = "numeric"
    TEXT = "text"
    TEXT_ARRAY = "text[]"


class EditorForm(forms.Form):
    error_css_class = "is-invalid"

    def clean(self):
        cleaned_data = super().clean()
        fields_with_errors = self.errors
        if "__all__" in self.errors:
            fields_with_errors = self.fields
        for field_name in fields_with_errors:
            try:
                field = self.fields[field_name]
                f_classes = field.widget.attrs.get("class", "").split(" ")
                f_classes.append(self.error_css_class)
                field.widget.attrs.update({"class": " ".join(f_classes)})
            except KeyError:
                continue
        return cleaned_data


class FormWithIdAttributePrefix(forms.Form):
    def __init__(self, *args, id_prefix: str = "", **kwargs):
        kwargs.update({"auto_id": f"{id_prefix}-id_%s"})
        super().__init__(*args, **kwargs)


class FormWithIdAttributeSuffix(forms.Form):
    def __init__(self, *args, id_suffix: str = "", **kwargs):
        kwargs.update({"auto_id": f"id_%s-{id_suffix}"})
        super().__init__(*args, **kwargs)


class OpenApiSpecificationBasedForm(EditorForm):
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

    def populate_form_fields(self, field_data: dict):
        for field_key, field_metadata in field_data.items():
            is_required = field_key in self.required_field_names
            field = self.get_field(field_key, field_metadata, is_required=is_required)
            self.fields.update({field_key: field})

    def get_data_for_form_fields(self) -> dict:
        field_data = (
            self.api_client.endpoint_definition.get_all_user_specifiable_fields()
        )
        return field_data

    def add_extra_metadata_to_field_data(self, field_data: dict):
        column_metadata = self.column_metadata_api_client.get_resources()
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

    def get_field(
        self, field_name: str, field_metadata: dict, is_required: bool = False
    ) -> forms.Field:
        field_components = self.get_components_for_enum_field(field_metadata)
        if not field_components:
            # Determine field, widget and/or widget CSS classes
            # from OpenAPI spec metadata.
            field_components = self.get_generic_components_for_field(
                field_name, field_metadata.get("format", "")
            )
        (
            field_class,
            widget_class,
            css_classes,
            extra_field_kwargs,
            extra_widget_kwargs,
            extra_widget_attrs,
        ) = field_components.values()
        if "title" not in field_metadata:
            field_metadata.update({"title": " ".join(field_name.split("_")).title()})

        # Build field kwargs
        kwargs = self.configure_field_kwargs(
            field_metadata,
            widget_class,
            css_classes,
            is_required,
            extra_field_kwargs=extra_field_kwargs,
            extra_widget_kwargs=extra_widget_kwargs,
            extra_widget_attrs=extra_widget_attrs,
        )

        field = field_class(**kwargs)
        category = field_metadata.get("category")
        if not category:
            category = UNKNOWN_ATTRIBUTE_CATEGORY
        field.category = category
        return field

    def get_generic_components_for_field(self, field_name: str, field_format: str):
        field_class = forms.CharField
        widget_class = None
        css_classes: list = ["form-control"]
        format_enum = None
        extra_field_kwargs = dict()
        extra_widget_kwargs = dict()
        extra_widget_attrs = dict()
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
            case OpenApiPropertyFormat.GEOMETRY:
                field_class = GeometryPointField
                widget_class = GeometryPointWidget
                extra_widget_attrs.update(
                    {
                        "data-multi-value-field": field_name,
                    }
                )
                extra_widget_kwargs.update(
                    {
                        "widgets": {
                            "latitude": forms.NumberInput(
                                attrs={
                                    "class": "form-control",
                                    "placeholder": "e.g. 51.5072",
                                    "step": "any",
                                    "min": -90,
                                    "max": 90,
                                }
                            ),
                            "longitude": forms.NumberInput(
                                attrs={
                                    "class": "form-control",
                                    "placeholder": "e.g. -0.1276",
                                    "step": "any",
                                    "min": -180,
                                    "max": 180,
                                }
                            ),
                        }
                    }
                )
            case OpenApiPropertyFormat.INTEGER:
                field_class = forms.IntegerField
                extra_field_kwargs.update({"min_value": 1, "step_size": 1})
            case OpenApiPropertyFormat.NUMERIC | OpenApiPropertyFormat.DOUBLE_PRECISION:
                field_class = forms.FloatField
                extra_widget_attrs.update({"step": "any"})
            case OpenApiPropertyFormat.TEXT_ARRAY | OpenApiPropertyFormat.JSONB:
                widget_class = forms.Textarea
        if not widget_class:
            widget_class = field_class.widget
        return {
            "field_class": field_class,
            "widget_class": widget_class,
            "css_classes": css_classes,
            "extra_field_kwargs": extra_field_kwargs,
            "extra_widget_kwargs": extra_widget_kwargs,
            "extra_widget_attrs": extra_widget_attrs,
        }

    def configure_field_kwargs(
        self,
        field_metadata: dict,
        widget_class,
        css_classes: list[str],
        is_required: bool,
        extra_field_kwargs: dict | None = None,
        extra_widget_kwargs: dict | None = None,
        extra_widget_attrs: dict | None = None,
    ):
        if not extra_field_kwargs:
            extra_field_kwargs = dict()
        if not extra_widget_kwargs:
            extra_widget_kwargs = dict()
        if not extra_widget_attrs:
            extra_widget_attrs = dict()
        kwargs = {
            "required": is_required,
            "widget": widget_class(
                attrs={"class": " ".join(css_classes), **extra_widget_attrs},
                **extra_widget_kwargs,
            ),
        }
        field_title = field_metadata.get("title")
        kwargs.update(
            {
                "label": field_title,
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

    def get_components_for_enum_field(self, field_metadata: dict):
        format = field_metadata.get("format", "")
        if not format.endswith("enum"):
            return
        field_class = EnumField
        field_enums = field_metadata.get("enum", [])
        if not field_enums:
            return
        choices = [
            (field_enum, field_enum.replace("_", " ")) for field_enum in field_enums
        ]
        choices.insert(0, ("", "None"))
        return {
            "field_class": field_class,
            "widget_class": SelectWithDisabledFirstOption,
            "css_classes": ["form-select"],
            "extra_field_kwargs": {
                "choices": choices,
            },
            "extra_widget_kwargs": dict(),
            "extra_widget_attrs": dict(),
        }


class SimpleOpenApiSpecificationBasedForm(OpenApiSpecificationBasedForm):
    def get_data_for_form_fields(self) -> dict:
        field_data = (
            self.api_client.endpoint_definition.get_all_user_specifiable_fields(
                include_one_to_many_fields=False
            )
        )
        foreign_key_fields = self.api_client.endpoint_definition.get_user_specifiable_foreign_key_fields()
        for field_name, field_metadata in foreign_key_fields.items():
            field_data.pop(field_name, None)
        return field_data


class SimpleOpenApiSpecificationBasedFormWithIdAttributePrefix(
    FormWithIdAttributePrefix, SimpleOpenApiSpecificationBasedForm
):
    pass


class SimpleOpenApiSpecificationBasedFormWithIdAttributeSuffix(
    FormWithIdAttributeSuffix, SimpleOpenApiSpecificationBasedForm
):
    pass


class OpenApiSpecificationCategoryBasedForm(OpenApiSpecificationBasedForm):
    def __init__(
        self,
        api_client: ApiClient,
        column_metadata_api_client: ColumnMetadataApiClient,
        category: str,
        *args,
        **kwargs,
    ):
        self.category = category
        super().__init__(api_client, column_metadata_api_client, *args, **kwargs)

    def get_data_for_form_fields(self) -> dict:
        field_data = super().get_data_for_form_fields()
        if self.category.lower() == UNKNOWN_ATTRIBUTE_CATEGORY.lower():
            column_metadata = self.column_metadata_api_client.get_resources()
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

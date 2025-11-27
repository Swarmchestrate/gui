from django.forms.formsets import BaseFormSet

from editor.api.base_api_clients import ApiClient, ColumnMetadataApiClient


class OpenApiDefinitionBasedFormSet(BaseFormSet):
    def __init__(
        self,
        api_client: ApiClient,
        column_metadata_api_client: ColumnMetadataApiClient,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.column_metadata_api_client = column_metadata_api_client

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs.update(
            {
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
            }
        )
        return kwargs

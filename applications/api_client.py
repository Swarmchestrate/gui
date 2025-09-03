from editor.api_client import ApiClient


class ApplicationApiClient(ApiClient):
    def __init__(self) -> None:
        super().__init__()
        self.definition_name = 'application'
        self.endpoint = 'application'
        self.id_field = 'application_id'
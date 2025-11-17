from abc import ABC, abstractmethod


class BaseApiEndpointClient(ABC):
    @abstractmethod
    def _prepare_update_data(self, data: dict) -> dict:
        pass

    @abstractmethod
    def get(self, registration_id: int, params: dict | None = None) -> dict:
        pass

    @abstractmethod
    def get_registrations_by_ids(self, registration_ids: list[int], params: dict | None = None) -> list[dict]:
        pass

    @abstractmethod
    def get_registrations(self, params: dict | None = None):
        pass

    @abstractmethod
    def register(self, data: dict) -> dict:
        pass

    @abstractmethod
    def bulk_register(self, data_list: list[dict]) -> list[int]:
        pass

    @abstractmethod
    def update(self, registration_id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, registration_id: int, params: dict = None):
        pass

    @abstractmethod
    def delete_many(self, registration_ids: list[int]):
        pass

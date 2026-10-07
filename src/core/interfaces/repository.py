from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class Repository(ABC, Generic[T]):

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def read_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
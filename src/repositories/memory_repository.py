from typing import Generic, TypeVar

from src.core.interfaces.repository import Repository


T = TypeVar("T")


class MemoryRepository(Repository[T], Generic[T]):

    def __init__(self):
        self._entities: dict[int, T] = {}
        self._next_id = 1

    def add(self, entity: T) -> None:
        entity_id = self._next_id

        # On donne un identifiant à l'objet
        entity.id = entity_id

        self._entities[entity_id] = entity

        self._next_id += 1

    def get_by_id(self, entity_id: int) -> T | None:
        return self._entities.get(entity_id)

    def read_all(self) -> list[T]:
        return list(self._entities.values())

    def update(self, entity: T) -> None:
        if not hasattr(entity, "id"):
            return

        if entity.id not in self._entities:
            return

        self._entities[entity.id] = entity

    def delete(self, entity_id: int) -> bool:
        if entity_id not in self._entities:
            return False

        del self._entities[entity_id]

        return True
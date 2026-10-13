from typing import Generic, TypeVar

from parc_vehicule.core import Repository

T = TypeVar("T")


class MemoryRepository(Repository[T], Generic[T]):

    def __init__(self):
        self._entities: dict[int, T] = {}
        self._next_id = 1

    def add(self, entity: T) -> int:
        if hasattr(entity, "id") and entity.id is not None:
            entity_id = entity.id
        else:
            entity_id = self._next_id

        entity.id = entity_id
        self._entities[entity_id] = entity

        if entity_id >= self._next_id:
            self._next_id = entity_id + 1

        return entity_id

    def get_by_id(self, entity_id: int) -> T | None:
        return self._entities.get(entity_id)

    def read_all(self) -> list[T]:
        return list(self._entities.values())

    def update(self, entity: T) -> bool:
        if not hasattr(entity, "id") or entity.id not in self._entities:
            return False
        self._entities[entity.id] = entity
        return True

    def delete(self, entity_id: int) -> bool:
        if entity_id not in self._entities:
            return False
        del self._entities[entity_id]
        return True

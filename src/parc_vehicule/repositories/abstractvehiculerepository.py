from abc import ABC, abstractmethod
from typing import Any, List, Optional


class AbstractVehicleRepository(ABC):

    @abstractmethod
    def add(self, vehicle: Any) -> None:
        pass

    @abstractmethod
    def get_by_id(self, vehicle_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def read_all(self) -> List[Any]:
        pass

    @abstractmethod
    def update(self, vehicle: Any) -> None:
        pass

    @abstractmethod
    def delete(self, vehicle_id: int) -> bool:
        pass

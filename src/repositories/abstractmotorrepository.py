class AbstractMotorRepository(ABC):

    @abstractmethod
    def add(self, motor: Any) -> None:
        pass

    @abstractmethod
    def get_by_id(self, motor_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def read_all(self) -> List[Any]:
        pass

    @abstractmethod
    def update(self, motor: Any) -> None:
        pass

    @abstractmethod
    def delete(self, motor_id: int) -> bool:
        pass
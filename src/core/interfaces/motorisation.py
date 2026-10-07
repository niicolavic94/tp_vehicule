from abc import ABC, abstractmethod

class Motorisation(ABC):

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def autonomie(self) -> float:
        pass
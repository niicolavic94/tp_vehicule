from abc import ABC, abstractmethod


class Motorisation(ABC):

    @property
    @abstractmethod
    def type(self) -> str:
        """Retourne le type de motorisation."""
        pass

    @abstractmethod
    def autonomie(self) -> float:
        """Retourne l'autonomie théorique en kilomètres."""
        pass
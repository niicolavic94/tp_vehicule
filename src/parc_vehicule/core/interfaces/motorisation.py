"""Définit l'interface des motorisations de véhicules."""

from abc import ABC, abstractmethod


class Motorisation(ABC):
    """Interface abstraite d'une motorisation de véhicule."""

    def __init__(self):
        self.id = None
        self.power = None

    @property
    @abstractmethod
    def type(self) -> str:
        """Retourne le type de motorisation."""
        pass

    @abstractmethod
    def autonomie(self) -> float:
        """Retourne l'autonomie théorique en kilomètres."""
        pass

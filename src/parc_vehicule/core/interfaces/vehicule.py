from abc import ABC, abstractmethod

from parc_vehicule.core.interfaces import Motorisation


class Vehicule(ABC):

    @property
    @abstractmethod
    def moteur(self) -> Motorisation:
        pass

    @property
    @abstractmethod
    def marque(self) -> str:
        pass

    @property
    @abstractmethod
    def modele(self) -> str:
        pass

    @property
    @abstractmethod
    def annee(self) -> int:
        pass

    @property
    @abstractmethod
    def kilometrage(self) -> float:
        pass

    @property
    @abstractmethod
    def volume_coffre(self) -> float:
        pass

    @property
    @abstractmethod
    def categorie(self) -> str:
        pass
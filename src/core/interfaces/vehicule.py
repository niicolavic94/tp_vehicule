from abc import ABC, abstractmethod
from src.models.motorisation import Motorisation

class Vehicule(ABC):

    #TYPE
    @property
    @abstractmethod
    def type(self) -> Motorisation:
        pass
    #MOTEUR
    @property
    @abstractmethod
    def moteur(self) -> Motorisation:
        pass
    #MARQUE
    @property
    @abstractmethod
    def marque(self) -> str:
        pass
    #MODELE
    @property
    @abstractmethod
    def modele(self) -> str:
        pass
    #ANNEE
    @property
    @abstractmethod
    def annee(self) -> int:
        pass
    #KM
    @property
    @abstractmethod
    def kilometrage(self) -> float:
        pass



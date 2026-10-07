from src.core.exceptions import VehiculeIntrouvableError
from src.core.interfaces.repository import Repository


class MemoryRepository(Repository):
    def __init__(self):
        self._vehicules = {}
        self._prochain_id = 1
#AJOUT
    def add(self, vehicule):
        vehicule.id = self._prochain_id
        self._vehicules[vehicule.id] = vehicule
        self._prochain_id += 1
        return vehicule
#SUPPRESSION
    def delete(self, vehicule_id: int) -> None:
        self.get(vehicule_id)  # lève l'erreur si l'id n'existe pas
        del self._vehicules[vehicule_id]
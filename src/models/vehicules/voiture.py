from src.core.interfaces.vehicule import Vehicule
from src.core.interfaces.motorisation import Motorisation
from src.core.exceptions import ValidationError

from src.utils.validators import (
    valider_texte,
    valider_annee,
    valider_positif,
    valider_positif_ou_nul
)


CATEGORIES = {
    "suv",
    "break",
    "berline",
    "citadine",
    "monospace"
}


class Voiture(Vehicule):

    def __init__(
        self,
        marque: str,
        modele: str,
        annee: int,
        kilometrage: float,
        volume_coffre: float,
        categorie: str,
        moteur: Motorisation
    ):
        self.id = None

        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.kilometrage = kilometrage
        self.volume_coffre = volume_coffre
        self.categorie = categorie
        self.moteur = moteur

    @property
    def marque(self) -> str:
        return self._marque

    @marque.setter
    def marque(self, valeur: str):
        self._marque = valider_texte(
            valeur,
            "La marque"
        )

    @property
    def modele(self) -> str:
        return self._modele

    @modele.setter
    def modele(self, valeur: str):
        self._modele = valider_texte(
            valeur,
            "Le modèle"
        )

    @property
    def annee(self) -> int:
        return self._annee

    @annee.setter
    def annee(self, valeur: int):
        self._annee = valider_annee(valeur)

    @property
    def kilometrage(self) -> float:
        return self._kilometrage

    @kilometrage.setter
    def kilometrage(self, valeur: float):
        self._kilometrage = valider_positif_ou_nul(
            valeur,
            "Le kilométrage"
        )

    @property
    def volume_coffre(self) -> float:
        return self._volume_coffre

    @volume_coffre.setter
    def volume_coffre(self, valeur: float):
        self._volume_coffre = valider_positif(
            valeur,
            "Le volume du coffre"
        )

    @property
    def categorie(self) -> str:
        return self._categorie

    @categorie.setter
    def categorie(self, valeur: str):
        valeur = valider_texte(
            valeur,
            "La catégorie"
        ).lower()

        if valeur not in CATEGORIES:
            raise ValidationError(
                f"Catégorie inconnue : {valeur}. "
                f"Catégories disponibles : {CATEGORIES}"
            )

        self._categorie = valeur

    @property
    def moteur(self) -> Motorisation:
        return self._moteur

    @moteur.setter
    def moteur(self, valeur: Motorisation):
        if not isinstance(valeur, Motorisation):
            raise TypeError(
                "Le moteur doit être une Motorisation."
            )

        self._moteur = valeur

    def __str__(self) -> str:
        return (
            f"{self.marque} {self.modele} "
            f"({self.annee}) - "
            f"{self.categorie} - "
            f"{self.volume_coffre} L - "
            f"{self.kilometrage} km - "
            f"{self.moteur.type}"
        )

    def __repr__(self) -> str:
        return self.__str__()
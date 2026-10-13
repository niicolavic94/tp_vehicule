from parc_vehicule.core.exceptions import ValidationError
from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.core.interfaces.vehicule import Vehicule
from parc_vehicule.utils.validators import (
    valider_texte,
    valider_annee,
    valider_positif,
    valider_positif_ou_nul,
)

CATEGORIES = {"suv", "break", "berline", "citadine", "monospace"}


class Voiture(Vehicule):

    def __init__(
        self,
        marque: str,
        modele: str,
        annee: int,
        moteur: Motorisation = None,
        kilometrage: float = 0,
        volume_coffre: float = 300,
        categorie: str = "berline",
        id: int = None,
    ):
        self.id = id
        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.kilometrage = kilometrage
        self.volume_coffre = volume_coffre
        self.categorie = categorie
        self.moteur = moteur

    # --- marque ---
    @property
    def marque(self) -> str:
        return self._marque

    @marque.setter
    def marque(self, valeur: str):
        self._marque = valider_texte(valeur, "La marque")

    @property
    def brand(self) -> str:
        return self._marque

    @brand.setter
    def brand(self, valeur: str):
        self.marque = valeur

    # --- modele ---
    @property
    def modele(self) -> str:
        return self._modele

    @modele.setter
    def modele(self, valeur: str):
        self._modele = valider_texte(valeur, "Le modèle")

    @property
    def model(self) -> str:
        return self._modele

    @model.setter
    def model(self, valeur: str):
        self.modele = valeur

    # --- annee ---
    @property
    def annee(self) -> int:
        return self._annee

    @annee.setter
    def annee(self, valeur: int):
        self._annee = valider_annee(valeur)

    @property
    def year(self) -> int:
        return self._annee

    @year.setter
    def year(self, valeur: int):
        self.annee = valeur

    # --- kilometrage ---
    @property
    def kilometrage(self) -> float:
        return self._kilometrage

    @kilometrage.setter
    def kilometrage(self, valeur: float):
        self._kilometrage = valider_positif_ou_nul(valeur, "Le kilométrage")

    # --- volume_coffre ---
    @property
    def volume_coffre(self) -> float:
        return self._volume_coffre

    @volume_coffre.setter
    def volume_coffre(self, valeur: float):
        self._volume_coffre = valider_positif(valeur, "Le volume du coffre")

    # --- categorie ---
    @property
    def categorie(self) -> str:
        return self._categorie

    @categorie.setter
    def categorie(self, valeur: str):
        valeur = valider_texte(valeur, "La catégorie").lower()
        if valeur not in CATEGORIES:
            raise ValidationError(
                f"Catégorie inconnue : {valeur}. "
                f"Catégories disponibles : {CATEGORIES}"
            )
        self._categorie = valeur

    # --- moteur ---
    @property
    def moteur(self) -> Motorisation:
        return self._moteur

    @moteur.setter
    def moteur(self, valeur):
        if valeur is not None and not isinstance(valeur, Motorisation):
            raise TypeError("Le moteur doit être une Motorisation.")
        self._moteur = valeur

    @property
    def motor(self) -> Motorisation:
        return self._moteur

    @motor.setter
    def motor(self, valeur):
        self.moteur = valeur

    # --- extras ---
    @property
    def type(self) -> str:
        return "Car"

    @property
    def autonomy(self) -> float:
        if self._moteur is None:
            return 0.0
        return self._moteur.autonomie()

    def __str__(self) -> str:
        if self._moteur is None:
            moteur_str = "sans motorisation"
        else:
            moteur_str = self._moteur.type
        return (
            f"{self.marque} {self.modele} "
            f"({self.annee}) - "
            f"{self.categorie} - "
            f"{self.volume_coffre} L - "
            f"{self.kilometrage} km - "
            f"{moteur_str}"
        )

    def __repr__(self) -> str:
        return self.__str__()

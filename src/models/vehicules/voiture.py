from src.core.interfaces.motorisation import Motorisation
from src.core.interfaces.vehicule import Vehicule


class Voiture(Vehicule):
    def __init__(self, marque, modele, annee, kilometrage, moteur,
                 volume_coffre_l, categorie):
        self.id = None  # attribué par le repository
        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.kilometrage = kilometrage
        self.moteur = moteur
        self.volume_coffre_l = volume_coffre_l
        self.categorie = categorie

    @property
    def marque(self) -> str:
        return self._marque

    @marque.setter
    def marque(self, valeur):
        self._marque = valider_texte(valeur, "La marque")

    @property
    def modele(self) -> str:
        return self._modele

    @modele.setter
    def modele(self, valeur):
        self._modele = valider_texte(valeur, "Le modèle")

    @property
    def annee(self) -> int:
        return self._annee

    @annee.setter
    def annee(self, valeur):
        self._annee = valider_annee(valeur)

    @property
    def kilometrage(self) -> float:
        return self._kilometrage

    @kilometrage.setter
    def kilometrage(self, valeur):
        self._kilometrage = valider_positif_ou_nul(valeur, "Le kilométrage")

    @property
    def moteur(self) -> Motorisation:
        return self._moteur

    @moteur.setter
    def moteur(self, valeur):
        if not isinstance(valeur, Motorisation):
            raise ValidationError("Le moteur doit être une Motorisation")
        self._moteur = valeur

    @property
    def volume_coffre_l(self) -> float:
        return self._volume_coffre_l

    @volume_coffre_l.setter
    def volume_coffre_l(self, valeur):
        self._volume_coffre_l = valider_positif(valeur, "Le volume de coffre")

    @property
    def categorie(self) -> str:
        return self._categorie

    @categorie.setter
    def categorie(self, valeur):
        valeur = valider_texte(valeur, "La catégorie").lower()
        if valeur not in CATEGORIES:
            raise ValidationError(f"Catégorie inconnue. Choix : {sorted(CATEGORIES)}")
        self._categorie = valeur

    def description(self) -> str:
        return (f"{self.marque} {self.modele} ({self.annee}) - {self.categorie} - "
                f"{self.moteur.type} - {self.kilometrage:.0f} km - "
                f"autonomie {self.moteur.autonomie():.0f} km")

    def __str__(self) -> str:
        return f"[{self.id}] {self.description()}"
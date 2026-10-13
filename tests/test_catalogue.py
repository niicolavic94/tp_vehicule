"""Tests automatisés du module test_catalogue."""
import pytest

from parc_vehicule.core import ValidationError
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules import Voiture


def test_validation_voiture_marque_vide():
    """Vérifie le comportement attendu."""
    with pytest.raises(ValidationError):
        Voiture(
            marque="",
            modele="Clio",
            annee=2020,
            moteur=Thermique(
                reservoir_l=40,
                consommation_l_100km=5,
            ),
        )
"""Tests automatisés du module test_catalogue."""
import pytest

from src.core.exceptions import ValidationError
from src.models.motorisations.thermique import Thermique
from src.models.vehicules.voiture import Voiture


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

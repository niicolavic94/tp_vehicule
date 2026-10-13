"""Tests de la fabrique de motorisations."""
import pytest

import parc_vehicule.services.usine as usine_module
from parc_vehicule.services.usine import Usine


class Faux:
    """Faux moteur qui garde ses paramètres."""

    def __init__(self, **params):
        self.params = params


@pytest.fixture(autouse=True)
def faux_moteurs(monkeypatch):
    """Remplace les vraies classes par des doublures."""
    for nom in ("Thermique", "Electrique", "Hybride"):
        monkeypatch.setattr(usine_module, nom, type(nom, (Faux,), {}))


@pytest.mark.parametrize(
    "type_moteur, attendu",
    [
        ("thermique", "Thermique"),
        ("electrique", "Electrique"),
        ("électrique", "Electrique"),
        ("hybride", "Hybride"),
        ("  HyBrIde  ", "Hybride"),
    ],
)
def test_creer_selon_le_type(type_moteur, attendu):
    moteur = Usine.creer(type_moteur, power=100)
    assert type(moteur).__name__ == attendu
    assert moteur.params == {"power": 100}


@pytest.mark.parametrize("type_invalide", ["diesel", "", None, 42])
def test_creer_type_invalide(type_invalide):
    with pytest.raises(ValueError, match="Type attendu"):
        Usine.creer(type_invalide)

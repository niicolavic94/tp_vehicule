"""Tests automatisés du module test_power."""
# pylint: disable=duplicate-code
import pytest

from parc_vehicule.core import ValidationError
from parc_vehicule.models import Hybride
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.thermique import Thermique


@pytest.mark.parametrize(
    "factory, kwargs, expected",
    [
        (
            Thermique,
            {
                "reservoir_l": 60,
                "consommation_l_100km": 5,
                "power": 130,
            },
            130,
        ),
        (
            Electrique,
            {
                "capacite_kwh": 60,
                "consommation_kwh_100km": 5,
                "power": 160,
            },
            160,
        ),
        (
            Hybride,
            {
                "reservoir_l": 40,
                "consommation_l_100km": 5,
                "capacite_kwh": 20,
                "consommation_kwh_100km": 4,
                "power": 200,
            },
            200,
        ),
    ],
)
def test_puissance_conforme(factory, kwargs, expected):
    """Vérifie le comportement attendu."""
    moteur = factory(**kwargs)

    assert moteur.power == expected


@pytest.mark.parametrize(
    "power",
    [0, -1, -100, "Toyota", None],
)
def test_thermique_rejette_puissance_invalide(power):
    """Vérifie le comportement attendu."""
    with pytest.raises((ValidationError, ValueError, TypeError)):
        Thermique(
            reservoir_l=60,
            consommation_l_100km=5,
            power=power,
        )


@pytest.mark.parametrize(
    "power",
    [0, -1, -100, "Toyota", None],
)
def test_electrique_rejette_puissance_invalide(power):
    """Vérifie le comportement attendu."""
    with pytest.raises((ValidationError, ValueError, TypeError)):
        Electrique(
            capacite_kwh=60,
            consommation_kwh_100km=5,
            power=power,
        )


@pytest.mark.parametrize(
    "power",
    [0, -1, -100, "Toyota", None],
)
def test_hybride_rejette_puissance_invalide(power):
    """Vérifie le comportement attendu."""
    with pytest.raises((ValidationError, ValueError, TypeError)):
        Hybride(
            reservoir_l=40,
            consommation_l_100km=5,
            capacite_kwh=20,
            consommation_kwh_100km=4,
            power=power,
        )

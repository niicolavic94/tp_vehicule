"""Tests automatisés du module test_autonomies."""


import pytest

from src.core.exceptions import ValidationError
from src.models.motorisations.electrique import Electrique
from src.models.motorisations.hybride import Hybride
from src.models.motorisations.thermique import Thermique


@pytest.mark.parametrize(
    "reservoir, consommation, expected",
    [
        (60, 5, 1200),
        (40, 8, 500),
        (50, 10, 500),
        (1, 4, 25),
    ],
)
def test_autonomie_thermique(reservoir, consommation, expected):
    """Vérifie le comportement attendu."""
    moteur = Thermique(
        reservoir_l=reservoir,
        consommation_l_100km=consommation,
    )

    assert moteur.autonomie() == expected
    assert moteur.total_autonomy == expected
    assert moteur.thermic_autonomy == expected


@pytest.mark.parametrize(
    "capacite, consommation, expected",
    [
        (60, 5, 1200),
        (50, 10, 500),
        (80, 20, 400),
        (30, 6, 500),
    ],
)
def test_autonomie_electrique(capacite, consommation, expected):
    """Vérifie le comportement attendu."""
    moteur = Electrique(
        capacite_kwh=capacite,
        consommation_kwh_100km=consommation,
    )

    assert moteur.autonomie() == expected
    assert moteur.total_autonomy == expected
    assert moteur.electric_autonomy == expected


@pytest.mark.parametrize(
    "reservoir, conso_thermique, capacite, conso_electrique, "
    "expected_thermique, expected_electrique",
    [
        (40, 5, 20, 4, 800, 500),
        (60, 6, 30, 5, 1000, 600),
        (50, 10, 40, 8, 500, 500),
    ],
)
def test_autonomie_hybride(
    reservoir,
    conso_thermique,
    capacite,
    conso_electrique,
    expected_thermique,
    expected_electrique,
):
    """Vérifie le comportement attendu."""
    moteur = Hybride(
        reservoir_l=reservoir,
        consommation_l_100km=conso_thermique,
        capacite_kwh=capacite,
        consommation_kwh_100km=conso_electrique,
    )

    assert moteur.thermic_autonomy == expected_thermique
    assert moteur.electric_autonomy == expected_electrique
    assert moteur.total_autonomy == (
        expected_thermique + expected_electrique
    )
    assert moteur.autonomie() == moteur.total_autonomy


@pytest.mark.parametrize(
    "reservoir, consommation",
    [
        (0, 5),
        (50, 0),
        (-1, 5),
        (50, -1),
    ],
)
def test_autonomie_thermique_rejette_valeurs_invalides(
    reservoir, consommation
):
    """Vérifie le comportement attendu."""
    with pytest.raises(ValidationError):
        Thermique(
            reservoir_l=reservoir,
            consommation_l_100km=consommation,
        )


@pytest.mark.parametrize(
    "capacite, consommation",
    [
        (0, 5),
        (50, 0),
        (-1, 5),
        (50, -1),
    ],
)
def test_autonomie_electrique_rejette_valeurs_invalides(
    capacite, consommation
):
    """Vérifie le comportement attendu."""
    with pytest.raises(ValidationError):
        Electrique(
            capacite_kwh=capacite,
            consommation_kwh_100km=consommation,
        )

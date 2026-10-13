"""Tests automatisés du module test_car_service."""
# pylint: disable=redefined-outer-name
import pytest
from parc_vehicule.services.catalogue import Catalogue

from parc_vehicule.core import ValidationError
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules import Voiture
from parc_vehicule.repositories import MemoryRepository


@pytest.fixture
def car_service():
    # Un nouveau catalogue pour isoler chaque test.
    """Définit le comportement de car service."""
    return Catalogue(MemoryRepository())


def nouvelle_voiture(marque="Toyota", modele="Corolla"):
    """Définit le comportement de nouvelle voiture."""
    return Voiture(
        marque=marque,
        modele=modele,
        annee=2022,
        moteur=Thermique(reservoir_l=50, consommation_l_100km=5),
        kilometrage=0,
        volume_coffre=300,
        categorie="berline",
    )


# CREATE


def test_create_car(car_service):
    """Vérifie le comportement attendu."""
    voiture = nouvelle_voiture()

    identifiant = car_service.ajouter(voiture)

    assert identifiant == 1
    assert voiture.id == identifiant
    assert car_service.chercher(identifiant) is voiture


def test_create_car_with_invalid_brand():
    """Vérifie le comportement attendu."""
    with pytest.raises(ValidationError):
        Voiture(
            marque="",
            modele="Corolla",
            annee=2022,
            moteur=Thermique(reservoir_l=50, consommation_l_100km=5),
        )


# GET


def test_get_existing_car(car_service):
    """Vérifie le comportement attendu."""
    voiture = nouvelle_voiture()
    identifiant = car_service.ajouter(voiture)

    resultat = car_service.chercher(identifiant)

    assert resultat == voiture


def test_get_unknown_car_returns_none(car_service):
    """Vérifie le comportement attendu."""
    assert car_service.chercher(999) is None


# FIND


def test_find_returns_all_cars(car_service):
    """Vérifie le comportement attendu."""
    voiture1 = nouvelle_voiture("Toyota", "Corolla")
    voiture2 = nouvelle_voiture("Renault", "Clio")

    car_service.ajouter(voiture1)
    car_service.ajouter(voiture2)

    resultat = car_service.lister()

    assert len(resultat) == 2
    assert voiture1 in resultat
    assert voiture2 in resultat


def test_find_empty_catalogue_returns_empty_list(car_service):
    """Vérifie le comportement attendu."""
    assert car_service.lister() == []


# DELETE


def test_delete_existing_car(car_service):
    """Vérifie le comportement attendu."""
    voiture = nouvelle_voiture()
    identifiant = car_service.ajouter(voiture)

    resultat = car_service.supprimer(identifiant)

    assert resultat is True
    assert car_service.chercher(identifiant) is None
    assert car_service.lister() == []


def test_delete_unknown_car_returns_false(car_service):
    """Vérifie le comportement attendu."""
    assert car_service.supprimer(999) is False


# UPDATE


def test_update_existing_car(car_service):
    """Vérifie le comportement attendu."""
    voiture = nouvelle_voiture()
    identifiant = car_service.ajouter(voiture)

    voiture.modele = "Yaris"

    assert car_service.modifier(voiture) is True
    assert car_service.chercher(identifiant).modele == "Yaris"


def test_update_unknown_car_returns_false(car_service):
    """Vérifie le comportement attendu."""
    voiture = nouvelle_voiture()
    voiture.id = 999

    assert car_service.modifier(voiture) is False

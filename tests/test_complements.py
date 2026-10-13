"""Tests complémentaires : connexion, contrats abstraits, modèles, validateurs."""
from unittest.mock import patch

import pytest

from parc_vehicule.core import ValidationError
from parc_vehicule.models import Hybride
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules import Voiture
from parc_vehicule.utils.validators import (
    valider_annee,
    valider_positif,
    valider_positif_ou_nul,
)


# ------------------------------------------------------- mysql_connection
def test_get_connection_utilise_les_variables_denvironnement(monkeypatch):
    from parc_vehicule.repositories import mysql_connection

    monkeypatch.setenv("DB_HOST", "db")
    monkeypatch.setenv("DB_PORT", "3307")
    monkeypatch.setenv("DB_NAME", "base")
    monkeypatch.setenv("DB_USER", "u")
    monkeypatch.setenv("DB_PASSWORD", "p")
    with patch.object(mysql_connection.mysql.connector, "connect") as connect:
        res = mysql_connection.get_connection()
    connect.assert_called_once_with(
        host="db", port=3307, database="base", user="u", password="p",
        autocommit=False, use_pure=True,
    )
    assert res is connect.return_value


def test_get_connection_valeurs_par_defaut(monkeypatch):
    from parc_vehicule.repositories import mysql_connection

    for var in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"):
        monkeypatch.delenv(var, raising=False)
    with patch.object(mysql_connection.mysql.connector, "connect") as connect:
        mysql_connection.get_connection()
    kwargs = connect.call_args.kwargs
    assert kwargs["host"] == "localhost"
    assert kwargs["port"] == 3306


# --------------------------------------------------------- contrats abstraits
def test_contrat_abstrait():
    from parc_vehicule.core.interfaces.repository import Repository
    cls = Repository
    with pytest.raises(TypeError):
        cls()  # non instanciable

    methodes = ("add", "get_by_id", "read_all", "update", "delete")
    Concrete = type("Concrete", (cls,), {
        m: (lambda self, *a, _m=m: getattr(cls, _m)(self, *a)) for m in methodes
    })
    obj = Concrete()
    assert obj.add(None) is None
    assert obj.get_by_id(1) is None
    assert obj.read_all() is None
    assert obj.update(None) is None
    assert obj.delete(1) is None


# ------------------------------------------------------------ motorisations
def test_thermique_proprietes():
    m = Thermique(50, 5, power=100)
    assert m.type == "thermique"
    assert m.autonomie() == 1000
    assert m.thermic_autonomy == 1000
    assert m.total_autonomy == 1000
    assert m.consumption_thermic == 5
    assert m.capacity_thermic == 50
    assert "Thermique" in str(m)


def test_electrique_proprietes():
    m = Electrique(60, 15, power=150)
    assert m.type == "electrique"
    assert m.autonomie() == 400
    assert m.electric_autonomy == 400
    assert m.total_autonomy == 400
    assert m.consumption_electric == 15
    assert m.capacity_electric == 60
    assert "Électrique" in str(m)


def test_hybride_proprietes():
    m = Hybride(40, 5, 10, 20, power=200)
    assert m.type == "hybride"
    assert m.autonomie_thermique() == 800
    assert m.autonomie_electrique() == 50
    assert m.autonomie() == 850
    assert m.thermic_autonomy == 800
    assert m.electric_autonomy == 50
    assert m.total_autonomy == 850
    assert m.consumption_thermic == 5
    assert m.capacity_thermic == 40
    assert m.consumption_electric == 20
    assert m.capacity_electric == 10
    assert "Hybride" in str(m)


@pytest.mark.parametrize("args", [(0, 5), (50, 0), (-1, 5)])
def test_thermique_invalide(args):
    with pytest.raises(ValidationError):
        Thermique(*args)


def test_electrique_puissance_invalide():
    with pytest.raises(ValidationError):
        Electrique(60, 15, power=0)


# ------------------------------------------------------------------ voiture
@pytest.fixture
def voiture():
    return Voiture("Renault", "Clio", 2020, moteur=Thermique(50, 5))


def test_voiture_alias_anglais(voiture):
    assert voiture.brand == "Renault"
    voiture.brand = "Peugeot"
    assert voiture.marque == "Peugeot"

    assert voiture.model == "Clio"
    voiture.model = "208"
    assert voiture.modele == "208"

    assert voiture.year == 2020
    voiture.year = 2021
    assert voiture.annee == 2021

    assert voiture.motor is voiture.moteur
    nouveau = Electrique(60, 15)
    voiture.motor = nouveau
    assert voiture.moteur is nouveau


def test_voiture_autonomy_et_type(voiture):
    assert voiture.type == "Car"
    assert voiture.autonomy == 1000
    voiture.moteur = None
    assert voiture.autonomy == 0.0


def test_voiture_str_repr(voiture):
    assert "Renault Clio (2020)" in str(voiture)
    assert repr(voiture) == str(voiture)
    voiture.moteur = None
    assert "sans motorisation" in str(voiture)


def test_voiture_moteur_type_invalide(voiture):
    with pytest.raises(TypeError):
        voiture.moteur = "pas un moteur"


def test_voiture_categorie_inconnue(voiture):
    with pytest.raises(ValidationError, match="Catégorie inconnue"):
        voiture.categorie = "fusée"


def test_voiture_categorie_normalisee(voiture):
    voiture.categorie = "  SUV "
    assert voiture.categorie == "suv"


@pytest.mark.parametrize("champ, valeur", [
    ("kilometrage", -1), ("volume_coffre", 0), ("annee", 1800), ("marque", " "),
])
def test_voiture_valeurs_invalides(voiture, champ, valeur):
    with pytest.raises(ValidationError):
        setattr(voiture, champ, valeur)


# --------------------------------------------------------------- validateurs
def test_valider_positif():
    assert valider_positif(3, "x") == 3
    for mauvais in (0, -2, "a", None):
        with pytest.raises(ValidationError):
            valider_positif(mauvais, "x")


def test_valider_positif_ou_nul():
    assert valider_positif_ou_nul(0, "x") == 0
    for mauvais in (-1, "a", None):
        with pytest.raises(ValidationError):
            valider_positif_ou_nul(mauvais, "x")


def test_valider_annee():
    assert valider_annee(1886) == 1886
    with pytest.raises(ValidationError):
        valider_annee(1885)
    with pytest.raises(ValidationError):
        valider_annee("2020")


# ---------------------------------------------------------- memory_repository
def test_memory_repository_conserve_un_id_existant():
    from parc_vehicule.repositories import MemoryRepository

    repo = MemoryRepository()
    v = Voiture("Renault", "Clio", 2020, id=10)
    assert repo.add(v) == 10
    nouveau = Voiture("Peugeot", "208", 2021)
    assert repo.add(nouveau) == 11  # le compteur repart après l'id explicite

"""Tests des dépôts base de données (connexion MySQL mockée)."""
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.models.motorisations.electrique import Electrique
from src.models.motorisations.hybride import Hybride
from src.models.motorisations.thermique import Thermique
from src.models.vehicules.voiture import Voiture
from src.repositories.databaserepository import (
    DatabaseMotorRepository,
    DatabaseVehicleRepository,
)


@pytest.fixture
def cur():
    """Curseur factice."""
    c = MagicMock()
    c.lastrowid = 7
    c.rowcount = 1
    return c


@pytest.fixture
def conn(cur):
    """Connexion factice renvoyant toujours le même curseur."""
    c = MagicMock()
    c.cursor.return_value = cur
    return c


def faux_moteur(**extra):
    base = {
        "type": "thermique",
        "power": 100,
        "consumption_thermic": 6.0,
        "capacity_thermic": 50.0,
        "consumption_electric": None,
        "capacity_electric": None,
        "id": None,
    }
    base.update(extra)
    return SimpleNamespace(**base)


# ---------------------------------------------------------------- moteurs
class TestMotorFromRow:
    def setup_method(self):
        self.repo = DatabaseMotorRepository(MagicMock())

    def test_none(self):
        assert self.repo._from_row(None) is None

    @pytest.mark.parametrize("typ", ["thermique", "Thermic"])
    def test_thermique(self, typ):
        m = self.repo._from_row((1, typ, 110, 6.0, 50.0, None, None))
        assert isinstance(m, Thermique)

    @pytest.mark.parametrize("typ", ["electrique", "Electric", "électrique"])
    def test_electrique(self, typ):
        m = self.repo._from_row((2, typ, None, None, None, 15.0, 60.0))
        assert isinstance(m, Electrique)

    @pytest.mark.parametrize("typ", ["hybride", "HYBRID"])
    def test_hybride(self, typ):
        m = self.repo._from_row((3, typ, 150, 5.0, 40.0, 14.0, 10.0))
        assert isinstance(m, Hybride)

    def test_type_inconnu(self):
        with pytest.raises(ValueError, match="inconnu"):
            self.repo._from_row((4, "vapeur", 100, 1, 1, 1, 1))


class TestMotorRepository:
    def test_add(self, conn, cur):
        motor = faux_moteur()
        assert DatabaseMotorRepository(conn).add(motor) == 7
        assert motor.id == 7
        conn.commit.assert_called_once()
        cur.close.assert_called_once()

    def test_add_erreur_rollback(self, conn, cur):
        cur.execute.side_effect = RuntimeError("boom")
        with pytest.raises(RuntimeError):
            DatabaseMotorRepository(conn).add(faux_moteur())
        conn.rollback.assert_called_once()
        cur.close.assert_called_once()

    def test_get_by_id(self, conn, cur):
        cur.fetchone.return_value = (1, "thermique", 100, 6.0, 50.0, None, None)
        assert isinstance(DatabaseMotorRepository(conn).get_by_id(1), Thermique)

    def test_get_by_id_absent(self, conn, cur):
        cur.fetchone.return_value = None
        assert DatabaseMotorRepository(conn).get_by_id(99) is None

    def test_read_all(self, conn, cur):
        cur.fetchall.return_value = [
            (1, "thermique", 100, 6.0, 50.0, None, None),
            (2, "electrique", 100, None, None, 15.0, 60.0),
        ]
        res = DatabaseMotorRepository(conn).read_all()
        assert [type(m) for m in res] == [Thermique, Electrique]

    @pytest.mark.parametrize("rowcount, attendu", [(1, True), (0, False)])
    def test_update(self, conn, cur, rowcount, attendu):
        cur.rowcount = rowcount
        assert DatabaseMotorRepository(conn).update(faux_moteur(id=1)) is attendu

    def test_update_erreur(self, conn, cur):
        cur.execute.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            DatabaseMotorRepository(conn).update(faux_moteur(id=1))
        conn.rollback.assert_called_once()

    @pytest.mark.parametrize("rowcount, attendu", [(1, True), (0, False)])
    def test_delete(self, conn, cur, rowcount, attendu):
        cur.rowcount = rowcount
        assert DatabaseMotorRepository(conn).delete(1) is attendu

    def test_delete_erreur(self, conn, cur):
        cur.execute.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            DatabaseMotorRepository(conn).delete(1)
        conn.rollback.assert_called_once()


# -------------------------------------------------------------- véhicules
ALL_COLS = {"id", "brand", "model", "year", "motor_id",
            "kilometrage", "volume_coffre", "categorie"}
MIN_COLS = {"id", "brand", "model", "year", "motor_id"}


def faux_vehicule(moteur="auto", **extra):
    base = dict(
        marque="Renault", modele="Clio", annee=2020, kilometrage=1000.0,
        volume_coffre=300.0, categorie="berline", id=3,
        moteur=faux_moteur() if moteur == "auto" else moteur,
    )
    base.update(extra)
    return SimpleNamespace(**base)


class TestVehicleRepository:
    def test_columns(self, conn, cur):
        cur.fetchall.return_value = [("id",), ("brand",)]
        assert DatabaseVehicleRepository(conn)._columns() == {"id", "brand"}
        cur.close.assert_called_once()

    @pytest.mark.parametrize("cols", [ALL_COLS, MIN_COLS])
    def test_add(self, conn, cur, monkeypatch, cols):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: cols)
        monkeypatch.setattr(repo, "_ensure_motor", lambda m: 5)
        v = faux_vehicule()
        assert repo.add(v) == 7
        assert v.id == 7
        sql, values = cur.execute.call_args[0]
        assert "INSERT INTO vehicles" in sql
        assert values[3] == 5
        assert len(values) == (7 if cols is ALL_COLS else 4)

    def test_add_erreur(self, conn, cur, monkeypatch):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: MIN_COLS)
        monkeypatch.setattr(repo, "_ensure_motor", lambda m: 5)
        cur.execute.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            repo.add(faux_vehicule())
        conn.rollback.assert_called_once()

    def test_ensure_motor_none(self, conn):
        with pytest.raises(ValueError, match="motorisation"):
            DatabaseVehicleRepository(conn)._ensure_motor(None)

    def test_ensure_motor_existant(self, conn, monkeypatch):
        monkeypatch.setattr(DatabaseMotorRepository, "get_by_id",
                            lambda self, i: object())
        assert DatabaseVehicleRepository(conn)._ensure_motor(
            faux_moteur(id=4)) == 4

    def test_ensure_motor_nouveau(self, conn, monkeypatch):
        monkeypatch.setattr(DatabaseMotorRepository, "add",
                            lambda self, m: 9)
        assert DatabaseVehicleRepository(conn)._ensure_motor(
            faux_moteur(id=None)) == 9

    def test_ensure_motor_id_introuvable_en_base(self, conn, monkeypatch):
        monkeypatch.setattr(DatabaseMotorRepository, "get_by_id",
                            lambda self, i: None)
        monkeypatch.setattr(DatabaseMotorRepository, "add",
                            lambda self, m: 11)
        assert DatabaseVehicleRepository(conn)._ensure_motor(
            faux_moteur(id=4)) == 11

    @pytest.mark.parametrize("cols", [ALL_COLS, MIN_COLS])
    def test_get_by_id_et_read_all(self, conn, cur, monkeypatch, cols):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: cols)
        monkeypatch.setattr(DatabaseMotorRepository, "get_by_id",
                            lambda self, i: Thermique(50.0, 6.0, power=100, id=1))
        cur.fetchall.return_value = [
            (3, "Renault", "Clio", 2020, 1000, 350, "citadine", 1),
        ]
        v = repo.get_by_id(3)
        assert isinstance(v, Voiture)
        assert v.marque == "Renault"
        assert len(repo.read_all()) == 1

    def test_get_by_id_absent(self, conn, cur, monkeypatch):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: MIN_COLS)
        cur.fetchall.return_value = []
        assert repo.get_by_id(99) is None

    def test_fetch_valeurs_par_defaut(self, conn, cur, monkeypatch):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: ALL_COLS)
        monkeypatch.setattr(DatabaseMotorRepository, "get_by_id",
                            lambda self, i: Thermique(50.0, 6.0, power=100, id=1))
        cur.fetchall.return_value = [
            (3, "Renault", "Clio", 2020, None, None, None, 1),
        ]
        v = repo.read_all()[0]
        assert v.kilometrage == 0
        assert v.volume_coffre == 300
        assert v.categorie == "berline"

    @pytest.mark.parametrize("cols", [ALL_COLS, MIN_COLS])
    @pytest.mark.parametrize("rowcount, attendu", [(1, True), (0, False)])
    def test_update(self, conn, cur, monkeypatch, cols, rowcount, attendu):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: cols)
        monkeypatch.setattr(repo, "_ensure_motor", lambda m: 5)
        cur.rowcount = rowcount
        assert repo.update(faux_vehicule()) is attendu
        assert "motor_id=%s" in cur.execute.call_args[0][0]

    def test_update_sans_moteur(self, conn, cur, monkeypatch):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: MIN_COLS)
        repo.update(faux_vehicule(moteur=None))
        assert "motor_id" not in cur.execute.call_args[0][0]

    def test_update_erreur(self, conn, cur, monkeypatch):
        repo = DatabaseVehicleRepository(conn)
        monkeypatch.setattr(repo, "_columns", lambda: MIN_COLS)
        monkeypatch.setattr(repo, "_ensure_motor", lambda m: 5)
        cur.execute.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            repo.update(faux_vehicule())
        conn.rollback.assert_called_once()

    @pytest.mark.parametrize("rowcount, attendu", [(1, True), (0, False)])
    def test_delete(self, conn, cur, rowcount, attendu):
        cur.rowcount = rowcount
        assert DatabaseVehicleRepository(conn).delete(1) is attendu

    def test_delete_erreur(self, conn, cur):
        cur.execute.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            DatabaseVehicleRepository(conn).delete(1)
        conn.rollback.assert_called_once()

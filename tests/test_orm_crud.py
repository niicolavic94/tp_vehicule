import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from parc_vehicule.database.database import Base
from parc_vehicule.database.models import MotorRecord, VehicleRecord
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules.voiture import Voiture
from parc_vehicule.services.catalogue import Catalogue
from parc_vehicule.services.motor_catalogue import MotorCatalogue, MotorInUseError


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as db:
        yield db
    engine.dispose()


def new_car(model="Clio", motor=None):
    return Voiture(
        "Renault",
        model,
        2020,
        moteur=motor or Thermique(50, 5),
        kilometrage=100,
        volume_coffre=300,
        categorie="berline",
    )


def test_vehicle_crud_and_motor_relation(session):
    cars = Catalogue(session)
    car = new_car()

    assert cars.ajouter(car) == car.id
    assert cars.chercher(car.id).modele == "Clio"
    assert cars.lister()[0].moteur.autonomie() == 1000
    assert cars.lister_par_motorisation(car.moteur.id)[0].id == car.id

    car.modele = "Captur"
    assert cars.modifier(car) is True
    assert cars.chercher(car.id).modele == "Captur"

    assert cars.supprimer(car.id) is True
    assert cars.chercher(car.id) is None
    assert cars.supprimer(car.id) is False


def test_vehicle_update_reuses_or_replaces_motor_without_orphans(session):
    cars = Catalogue(session)
    car = new_car()
    cars.ajouter(car)
    original_motor_id = car.moteur.id

    unchanged = cars.chercher(car.id)
    cars.modifier(unchanged)
    assert session.scalar(select(func.count()).select_from(MotorRecord)) == 1

    replacement = new_car(motor=Thermique(60, 6))
    replacement.id = car.id
    assert cars.modifier(replacement) is True
    assert session.scalar(select(func.count()).select_from(MotorRecord)) == 1
    assert cars.chercher(car.id).moteur.id != original_motor_id


def test_motor_crud_refuses_delete_while_in_use(session):
    cars = Catalogue(session)
    motors = MotorCatalogue(session)
    motor = Thermique(50, 5)
    motors.ajouter(motor)
    car = new_car(motor=motor)
    cars.ajouter(car)

    assert motors.chercher(motor.id).autonomie() == 1000
    with pytest.raises(MotorInUseError):
        motors.supprimer(motor.id)
    assert motors.modifier(motor.id, Thermique(60, 6)) is True
    assert motors.chercher(motor.id).autonomie() == 1000

    cars.supprimer(car.id)
    assert motors.supprimer(motor.id) is True
    assert motors.chercher(motor.id) is None


def test_vehicle_service_requires_a_motor(session):
    car = new_car()
    car.moteur = None

    with pytest.raises(ValueError, match="motorisation"):
        Catalogue(session).ajouter(car)


def test_orm_records_match_existing_database_schema():
    motor_columns = set(MotorRecord.__table__.columns.keys())
    vehicle_columns = set(VehicleRecord.__table__.columns.keys())

    assert motor_columns == {
        "id",
        "type",
        "power",
        "consumption_thermic",
        "capacity_thermic",
        "consumption_electric",
        "capacity_electric",
    }
    assert vehicle_columns == {
        "id",
        "brand",
        "model",
        "year",
        "motor_id",
        "kilometrage",
        "volume_coffre",
        "categorie",
    }

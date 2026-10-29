import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from parc_vehicule.database.database import Base, get_db
from parc_vehicule.database.models import VehicleRecord
from parc_vehicule.main import app
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules.voiture import Voiture
from parc_vehicule.routers.cars import VoitureCreate, update as update_car
from parc_vehicule.routers.motors import MoteurThermiqueCreate
from parc_vehicule.schemas.car import Car


@pytest.fixture
def api_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            yield client, engine
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def voiture_payload(reservoir=50):
    return VoitureCreate(
        marque="Renault",
        modele="Clio",
        annee=2020,
        kilometrage=10,
        volume_coffre=300,
        categorie="berline",
        moteur={
            "type": "thermique",
            "reservoir_l": reservoir,
            "consommation_l_100km": 5,
        },
    )


def test_update_car_sends_motor_data_to_service():
    motor = Thermique(50, 5, id=8)
    existing = Voiture("Renault", "Clio", 2020, moteur=motor, id=1)
    service = SimpleNamespace(
        chercher=MagicMock(return_value=existing),
        modifier=MagicMock(return_value=True),
        motors=MagicMock(),
    )

    asyncio.run(update_car(1, voiture_payload(), service))

    saved_car = service.modifier.call_args.args[0]
    assert saved_car.moteur is not motor
    assert saved_car.moteur.reservoir_l == motor.reservoir_l


def test_update_car_passes_replacement_to_database_service():
    motor = Thermique(50, 5, id=8)
    existing = Voiture("Renault", "Clio", 2020, moteur=motor, id=1)
    service = SimpleNamespace(
        chercher=MagicMock(return_value=existing),
        motors=MagicMock(),
    )

    def update(vehicle):
        vehicle.moteur.id = 9
        return True

    service.modifier = MagicMock(side_effect=update)

    asyncio.run(update_car(1, voiture_payload(reservoir=60), service))

    assert service.modifier.call_args.args[0].moteur.id == 9


def test_motor_power_must_be_positive():
    with pytest.raises(PydanticValidationError):
        MoteurThermiqueCreate.model_validate(
            {
                "type": "thermique",
                "reservoir_l": 50,
                "consommation_l_100km": 5,
                "power": 0,
            }
        )


def test_car_schema_can_validate_an_object():
    car = SimpleNamespace(brand="Renault", model="Clio", year=2020, motor_id=3)

    assert Car.model_validate(car).motor_id == 3


def test_api_crud_uses_orm_backed_services(api_client):
    client, engine = api_client
    motor_response = client.post(
        "/motorisations/",
        json={
            "type": "thermique",
            "reservoir_l": 50,
            "consommation_l_100km": 5,
            "power": 100,
        },
    )
    assert motor_response.status_code == 201
    motor = motor_response.json()
    motor_id = motor["id"]

    car_payload = {
        "marque": "Renault",
        "modele": "Clio",
        "annee": 2020,
        "kilometrage": 100,
        "volume_coffre": 300,
        "categorie": "berline",
        "moteur": {
            "type": "thermique",
            "reservoir_l": 50,
            "consommation_l_100km": 5,
        },
    }
    car_response = client.post("/cars/", json=car_payload)
    assert car_response.status_code == 201
    car = car_response.json()
    car_id = car["id"]
    with Session(engine) as session:
        linked_motor_id = session.scalar(
            select(VehicleRecord.motor_id).where(VehicleRecord.id == car_id)
        )

    assert client.get(f"/cars/{car_id}").json()["modele"] == "Clio"
    assert len(client.get("/cars/").json()) == 1
    assert client.get(f"/motorisations/{motor_id}").json()["id"] == motor_id
    assert len(client.get(f"/motorisations/{linked_motor_id}/cars").json()) == 1

    car_payload["modele"] = "Captur"
    assert client.put(f"/cars/{car_id}", json=car_payload).status_code == 200
    assert client.get(f"/cars/{car_id}").json()["modele"] == "Captur"

    assert client.put(
        f"/motorisations/{motor_id}",
        json={
            "type": "thermique",
            "reservoir_l": 60,
            "consommation_l_100km": 6,
            "power": 110,
        },
    ).status_code == 200
    assert len(client.get("/motorisations/").json()) == 2
    assert client.delete(f"/motorisations/{linked_motor_id}").status_code == 409
    assert client.delete(f"/cars/{car_id}").status_code == 204
    assert client.delete(f"/motorisations/{linked_motor_id}").status_code == 204

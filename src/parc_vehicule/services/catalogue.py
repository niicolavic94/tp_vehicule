"""Opérations CRUD des véhicules avec la session SQLAlchemy."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from parc_vehicule.database.models import MotorRecord, VehicleRecord
from parc_vehicule.models.vehicules.voiture import Voiture


def _motor_signature(motor) -> tuple:
    return (
        motor.type,
        getattr(motor, "power", None),
        getattr(motor, "consumption_thermic", None),
        getattr(motor, "capacity_thermic", None),
        getattr(motor, "consumption_electric", None),
        getattr(motor, "capacity_electric", None),
    )


class Catalogue:
    """Couche service assurant les opérations CRUD sur les véhicules."""

    def __init__(self, session: Session):
        self.session = session

    def ajouter(self, vehicle: Voiture) -> int:
        if vehicle.moteur is None:
            raise ValueError("Un véhicule doit avoir une motorisation.")

        motor = self._find_or_create_motor(vehicle.moteur)
        record = VehicleRecord(
            brand=vehicle.marque,
            model=vehicle.modele,
            year=vehicle.annee,
            kilometrage=vehicle.kilometrage,
            volume_coffre=vehicle.volume_coffre,
            categorie=vehicle.categorie,
            motor=motor,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        vehicle.id = record.id
        vehicle.moteur.id = motor.id
        return record.id

    def lister(self) -> list[Voiture]:
        records = self.session.scalars(
            select(VehicleRecord).options(selectinload(VehicleRecord.motor))
        ).all()
        return [record.to_domain() for record in records]

    def chercher(self, vehicle_id: int) -> Voiture | None:
        record = self.session.scalar(
            select(VehicleRecord)
            .options(selectinload(VehicleRecord.motor))
            .where(VehicleRecord.id == vehicle_id)
        )
        return record.to_domain() if record is not None else None

    def modifier(self, vehicle: Voiture) -> bool:
        record = self.session.scalar(
            select(VehicleRecord)
            .options(
                selectinload(VehicleRecord.motor).selectinload(
                    MotorRecord.vehicles
                )
            )
            .where(VehicleRecord.id == vehicle.id)
        )
        if record is None:
            return False
        if vehicle.moteur is None:
            raise ValueError("Un véhicule doit avoir une motorisation.")

        previous_motor = record.motor
        record.brand = vehicle.marque
        record.model = vehicle.modele
        record.year = vehicle.annee
        record.kilometrage = vehicle.kilometrage
        record.volume_coffre = vehicle.volume_coffre
        record.categorie = vehicle.categorie

        if _motor_signature(previous_motor.to_domain()) != _motor_signature(
            vehicle.moteur
        ):
            record.motor = self._find_or_create_motor(vehicle.moteur)
            self.session.flush()
            if not previous_motor.vehicles:
                self.session.delete(previous_motor)

        self.session.commit()
        return True

    def supprimer(self, vehicle_id: int) -> bool:
        record = self.session.get(VehicleRecord, vehicle_id)
        if record is None:
            return False
        self.session.delete(record)
        self.session.commit()
        return True

    def lister_par_motorisation(self, motor_id: int) -> list[Voiture]:
        records = self.session.scalars(
            select(VehicleRecord)
            .options(selectinload(VehicleRecord.motor))
            .where(VehicleRecord.motor_id == motor_id)
        ).all()
        return [record.to_domain() for record in records]

    def _find_or_create_motor(self, motor) -> MotorRecord:
        if motor.id is not None:
            record = self.session.get(MotorRecord, motor.id)
            if record is not None:
                return record
        record = MotorRecord.from_domain(motor)
        self.session.add(record)
        self.session.flush()
        motor.id = record.id
        return record

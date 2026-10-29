"""Opérations CRUD des motorisations avec la session SQLAlchemy."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.database.models import MotorRecord, VehicleRecord


class MotorInUseError(Exception):
    """Signale qu'une motorisation est encore liée à un véhicule."""


class MotorCatalogue:
    """Couche service assurant les opérations CRUD sur les motorisations."""

    def __init__(self, session: Session):
        self.session = session

    def ajouter(self, motor: Motorisation) -> int:
        record = MotorRecord.from_domain(motor)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        motor.id = record.id
        return record.id

    def lister(self) -> list[Motorisation]:
        records = self.session.scalars(select(MotorRecord)).all()
        return [record.to_domain() for record in records]

    def chercher(self, motor_id: int) -> Motorisation | None:
        record = self.session.get(MotorRecord, motor_id)
        return record.to_domain() if record is not None else None

    def modifier(self, motor_id: int, motor: Motorisation) -> bool:
        record = self.session.get(MotorRecord, motor_id)
        if record is None:
            return False

        replacement = MotorRecord.from_domain(motor)
        record.type = replacement.type
        record.power = replacement.power
        record.consumption_thermic = replacement.consumption_thermic
        record.capacity_thermic = replacement.capacity_thermic
        record.consumption_electric = replacement.consumption_electric
        record.capacity_electric = replacement.capacity_electric
        self.session.commit()
        return True

    def supprimer(self, motor_id: int) -> bool:
        record = self.session.get(MotorRecord, motor_id)
        if record is None:
            return False
        if self.session.scalar(
            select(func.count())
            .select_from(VehicleRecord)
            .where(VehicleRecord.motor_id == motor_id)
        ):
            raise MotorInUseError(
                "Cette motorisation est encore utilisée par un véhicule"
            )
        self.session.delete(record)
        self.session.commit()
        return True

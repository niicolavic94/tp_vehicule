from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.database.database import Base
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules.voiture import Voiture


class MotorRecord(Base):
    __tablename__ = "motors"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    power: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    consumption_thermic: Mapped[float | None] = mapped_column(Numeric(6, 2))
    capacity_thermic: Mapped[float | None] = mapped_column(Numeric(6, 2))
    consumption_electric: Mapped[float | None] = mapped_column(Numeric(6, 2))
    capacity_electric: Mapped[float | None] = mapped_column(Numeric(6, 2))

    vehicles: Mapped[list["VehicleRecord"]] = relationship(
        back_populates="motor",
    )

    def to_domain(self) -> Motorisation:
        motor_type = self.type.lower()
        power = self.power if self.power else None
        kwargs = {} if power is None else {"power": power}

        if motor_type in ("thermique", "thermic"):
            motor = Thermique(
                float(self.capacity_thermic),
                float(self.consumption_thermic),
                **kwargs,
            )
        elif motor_type in ("electrique", "electric", "électrique"):
            motor = Electrique(
                float(self.capacity_electric),
                float(self.consumption_electric),
                **kwargs,
            )
        elif motor_type in ("hybride", "hybrid"):
            motor = Hybride(
                float(self.capacity_thermic),
                float(self.consumption_thermic),
                float(self.capacity_electric),
                float(self.consumption_electric),
                **kwargs,
            )
        else:
            raise ValueError(f"Type de motorisation inconnu : {self.type!r}")

        motor.id = self.id
        return motor

    @classmethod
    def from_domain(cls, motor: Motorisation) -> "MotorRecord":
        return cls(
            type=motor.type,
            power=getattr(motor, "power", None) or 0,
            consumption_thermic=getattr(motor, "consumption_thermic", None),
            capacity_thermic=getattr(motor, "capacity_thermic", None),
            consumption_electric=getattr(motor, "consumption_electric", None),
            capacity_electric=getattr(motor, "capacity_electric", None),
        )


class VehicleRecord(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    motor_id: Mapped[int] = mapped_column(
        ForeignKey("motors.id", ondelete="RESTRICT", onupdate="CASCADE")
    )
    kilometrage: Mapped[float] = mapped_column(
        Numeric(10, 2), default=0, server_default="0"
    )
    volume_coffre: Mapped[float] = mapped_column(
        Numeric(10, 2), default=300, server_default="300"
    )
    categorie: Mapped[str] = mapped_column(
        String(30), default="berline", server_default="berline"
    )

    motor: Mapped[MotorRecord] = relationship(back_populates="vehicles")

    @property
    def marque(self) -> str:
        return self.brand

    @property
    def modele(self) -> str:
        return self.model

    @property
    def annee(self) -> int:
        return self.year

    def to_domain(self) -> Voiture:
        return Voiture(
            marque=self.brand,
            modele=self.model,
            annee=self.year,
            moteur=self.motor.to_domain(),
            kilometrage=float(self.kilometrage),
            volume_coffre=float(self.volume_coffre),
            categorie=self.categorie,
            id=self.id,
        )

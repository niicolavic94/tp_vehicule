from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.utils.validators import valider_positif

_MISSING = object()


class Electrique(Motorisation):

    def __init__(
        self,
        capacite_kwh: float,
        consommation_kwh_100km: float,
        power=_MISSING,
        id: int = None,
    ):
        self.capacite_kwh = valider_positif(capacite_kwh, "La capacité de batterie")
        self.consommation_kwh_100km = valider_positif(consommation_kwh_100km, "La consommation électrique")
        self.power = valider_positif(power, "La puissance") if power is not _MISSING else None
        self.id = id

    @property
    def type(self) -> str:
        return "electrique"

    def autonomie(self) -> float:
        return self.capacite_kwh / self.consommation_kwh_100km * 100

    @property
    def electric_autonomy(self) -> float:
        return self.autonomie()

    @property
    def total_autonomy(self) -> float:
        return self.autonomie()

    @property
    def consumption_electric(self) -> float:
        return self.consommation_kwh_100km

    @property
    def capacity_electric(self) -> float:
        return self.capacite_kwh

    def __str__(self) -> str:
        return (
            f"Électrique - "
            f"Batterie : {self.capacite_kwh} kWh - "
            f"Consommation : {self.consommation_kwh_100km} kWh/100km"
        )

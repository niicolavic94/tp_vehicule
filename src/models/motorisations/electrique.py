from src.core.interfaces.motorisation import Motorisation
from src.utils.validators import valider_positif


class Electrique(Motorisation):

    def __init__(
        self,
        capacite_kwh: float,
        consommation_kwh_100km: float
    ):
        self.capacite_kwh = valider_positif(
            capacite_kwh,
            "La capacité de batterie"
        )

        self.consommation_kwh_100km = valider_positif(
            consommation_kwh_100km,
            "La consommation électrique"
        )

    @property
    def type(self) -> str:
        return "electrique"

    def autonomie(self) -> float:
        return (
            self.capacite_kwh
            / self.consommation_kwh_100km
            * 100
        )

    def __str__(self) -> str:
        return (
            f"Électrique - "
            f"Batterie : {self.capacite_kwh} kWh - "
            f"Consommation : "
            f"{self.consommation_kwh_100km} kWh/100km"
        )
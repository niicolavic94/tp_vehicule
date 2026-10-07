from src.core.interfaces.motorisation import Motorisation
from src.models.motorisations.thermique import Thermique
from src.models.motorisations.electrique import Electrique


class Hybride(Motorisation):

    def __init__(
        self,
        reservoir_l: float,
        consommation_l_100km: float,
        capacite_kwh: float,
        consommation_kwh_100km: float
    ):
        self.thermique = Thermique(
            reservoir_l,
            consommation_l_100km
        )

        self.electrique = Electrique(
            capacite_kwh,
            consommation_kwh_100km
        )

    @property
    def type(self) -> str:
        return "hybride"

    def autonomie_thermique(self) -> float:
        return self.thermique.autonomie()

    def autonomie_electrique(self) -> float:
        return self.electrique.autonomie()

    def autonomie(self) -> float:
        return (
            self.autonomie_thermique()
            + self.autonomie_electrique()
        )

    def __str__(self) -> str:
        return (
            f"Hybride - "
            f"Thermique : {self.thermique.reservoir_l} L, "
            f"{self.thermique.consommation_l_100km} L/100km - "
            f"Électrique : {self.electrique.capacite_kwh} kWh, "
            f"{self.electrique.consommation_kwh_100km} kWh/100km"
        )
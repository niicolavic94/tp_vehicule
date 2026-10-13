from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.utils.validators import valider_positif

_MISSING = object()


class Thermique(Motorisation):

    def __init__(
        self,
        reservoir_l: float,
        consommation_l_100km: float,
        power=_MISSING,
        id: int = None,
    ):
        self.reservoir_l = valider_positif(reservoir_l, "Le réservoir")
        self.consommation_l_100km = valider_positif(consommation_l_100km, "La consommation thermique")
        if power is not _MISSING:
            self.power = valider_positif(power, "La puissance")
        else:
            self.power = None
        self.id = id

    @property
    def type(self) -> str:
        return "thermique"

    def autonomie(self) -> float:
        return self.reservoir_l / self.consommation_l_100km * 100

    @property
    def thermic_autonomy(self) -> float:
        return self.autonomie()

    @property
    def total_autonomy(self) -> float:
        return self.autonomie()

    @property
    def consumption_thermic(self) -> float:
        return self.consommation_l_100km

    @property
    def capacity_thermic(self) -> float:
        return self.reservoir_l

    def __str__(self) -> str:
        return (
            f"Thermique - "
            f"Réservoir : {self.reservoir_l} L - "
            f"Consommation : {self.consommation_l_100km} L/100km"
        )

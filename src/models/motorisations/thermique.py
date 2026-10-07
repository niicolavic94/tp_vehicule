from src.core.exceptions import ValidationError
from src.core.interfaces.motorisation import Motorisation
from src.utils.validators import valider_positif


class Thermique(Motorisation):

    def __init__(
        self,
        reservoir_l: float,
        consommation_l_100km: float
    ):
        self.reservoir_l = valider_positif(
            reservoir_l,
            "Le réservoir"
        )

        self.consommation_l_100km = valider_positif(
            consommation_l_100km,
            "La consommation thermique"
        )

    @property
    def type(self) -> str:
        return "thermique"

    def autonomie(self) -> float:
        return (
            self.reservoir_l
            / self.consommation_l_100km
            * 100
        )

    def __str__(self) -> str:
        return (
            f"Thermique - "
            f"Réservoir : {self.reservoir_l} L - "
            f"Consommation : {self.consommation_l_100km} L/100km"
        )
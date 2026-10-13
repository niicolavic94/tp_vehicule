from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.utils.validators import valider_positif

_MISSING = object()


class Hybride(Motorisation):

    def __init__(
        self,
        reservoir_l: float,
        consommation_l_100km: float,
        capacite_kwh: float,
        consommation_kwh_100km: float,
        power=_MISSING,
        id: int = None,
    ):
        self.thermique = Thermique(reservoir_l, consommation_l_100km)
        self.electrique = Electrique(capacite_kwh, consommation_kwh_100km)
        self.power = valider_positif(power, "La puissance") if power is not _MISSING else None
        self.id = id

    @property
    def type(self) -> str:
        return "hybride"

    def autonomie_thermique(self) -> float:
        return self.thermique.autonomie()

    def autonomie_electrique(self) -> float:
        return self.electrique.autonomie()

    def autonomie(self) -> float:
        return self.autonomie_thermique() + self.autonomie_electrique()

    @property
    def thermic_autonomy(self) -> float:
        return self.autonomie_thermique()

    @property
    def electric_autonomy(self) -> float:
        return self.autonomie_electrique()

    @property
    def total_autonomy(self) -> float:
        return self.autonomie()

    @property
    def consumption_thermic(self) -> float:
        return self.thermique.consommation_l_100km

    @property
    def capacity_thermic(self) -> float:
        return self.thermique.reservoir_l

    @property
    def consumption_electric(self) -> float:
        return self.electrique.consommation_kwh_100km

    @property
    def capacity_electric(self) -> float:
        return self.electrique.capacite_kwh

    def __str__(self) -> str:
        return (
            f"Hybride - "
            f"Thermique : {self.thermique.reservoir_l} L, "
            f"{self.thermique.consommation_l_100km} L/100km - "
            f"Électrique : {self.electrique.capacite_kwh} kWh, "
            f"{self.electrique.consommation_kwh_100km} kWh/100km"
        )

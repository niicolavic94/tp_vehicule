from src.models.motorisations.thermique import Thermique
from src.models.motorisations.electrique import Electrique


class Hybride(Thermique, Electrique):
    @property
    def type(self) -> str:
        return "hybride"

    def autonomie(self) -> float:
        return self.autonomie_thermique() + self.autonomie_electrique()
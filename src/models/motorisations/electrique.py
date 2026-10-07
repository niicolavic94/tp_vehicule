from src.core.interfaces.motorisation import Motorisation
from src.core.exceptions import ValidationError


class Electrique(Motorisation):
    def __init__(self, capacite_kwh: float, consommation_kwh_100km: float, **kwargs):
        super().__init__(**kwargs)
        self.capacite_kwh = capacite_kwh
        self.consommation_kwh_100km = consommation_kwh_100km

#CAPACITE
    @property
    def capacite_kwh(self) -> float:
        return self._capacite_kwh

    @capacite_kwh.setter
    def capacite_kwh(self, valeur: float):
        if valeur <= 0:
            raise ValidationError("La capacité de la batterie doit être positive")
        self._capacite_kwh = valeur
#CONSOMMATION
    @property
    def consommation_kwh_100km(self) -> float:
        return self._consommation_kwh_100km

    @consommation_kwh_100km.setter
    def consommation_kwh_100km(self, valeur: float):
        if valeur <= 0:
            raise ValidationError("La consommation doit être positive")
        self._consommation_kwh_100km = valeur

    @property
    def type(self) -> str:
        return "electrique"

    def autonomie_electrique(self) -> float:
        return self.capacite_kwh / self.consommation_kwh_100km * 100

    def autonomie(self) -> float:
        return self.autonomie_electrique()
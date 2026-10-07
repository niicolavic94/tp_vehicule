from src.core.interfaces.motorisation import Motorisation


class Thermique(Motorisation):
    def __init__(self, reservoir_l: float, consommation_l_100km: float, **kwargs):
        super().__init__(**kwargs)
        self.reservoir_l = reservoir_l
        self.consommation_l_100km = consommation_l_100km

#CAPACITE

    @property
    def reservoir_l(self) -> float:
        return self._reservoir_l

    @reservoir_l.setter
    def reservoir_l(self, valeur: float):
        if valeur <= 0:
            raise ValidationError("Le réservoir doit être positif")
        self._reservoir_l = valeur

#CONSOMMATION

    @property
    def consommation_l_100km(self) -> float:
        return self._consommation_l_100km

    @consommation_l_100km.setter
    def consommation_l_100km(self, valeur: float):
        if valeur <= 0:
            raise ValidationError("La consommation doit être positive")
        self._consommation_l_100km = valeur

    @property
    def type(self) -> str:
        return "thermique"

    def autonomie_thermique(self) -> float:
        return self.reservoir_l / self.consommation_l_100km * 100

    def autonomie(self) -> float:
        return self.autonomie_thermique()
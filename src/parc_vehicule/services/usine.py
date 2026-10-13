import parc_vehicule.services.usine as _self_module

from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique

_ALIASES = {
    "thermique": "Thermique",
    "electrique": "Electrique",
    "électrique": "Electrique",
    "hybride": "Hybride",
}


class Usine:

    MOTEURS = {
        "thermique": Thermique,
        "electrique": Electrique,
        "électrique": Electrique,
        "hybride": Hybride,
    }

    @staticmethod
    def creer(type_moteur, **kwargs):
        if not isinstance(type_moteur, str) or not type_moteur.strip():
            raise ValueError(f"Type attendu parmi {list(_ALIASES)}, reçu : {type_moteur!r}")
        cle = type_moteur.strip().lower()
        class_name = _ALIASES.get(cle)
        if class_name is None:
            raise ValueError(f"Type attendu parmi {list(_ALIASES)}, reçu : {type_moteur!r}")
        cls = getattr(_self_module, class_name)
        return cls(**kwargs)

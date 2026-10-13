"""Définit les éléments du module src models __init__."""

from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules.voiture import Voiture

__all__ = ["Electrique", "Hybride", "Thermique", "Voiture"]

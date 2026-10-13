"""Interfaces abstraites."""

from parc_vehicule.core.interfaces.motorisation import Motorisation
from parc_vehicule.core.interfaces.repository import Repository
from parc_vehicule.core.interfaces.vehicule import Vehicule

__all__ = ["Motorisation", "Repository", "Vehicule"]
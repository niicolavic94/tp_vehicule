
"""Définit la couche service du catalogue des véhicules."""

from abc import ABC


class Catalogue(ABC):
    """Couche service qui centralise les opérations du catalogue."""

    def __init__(self, vehicle_repository, motor_repository=None):
        """Initialise le catalogue avec ses dépôts."""
        self.vehicles = vehicle_repository
        self.motors = motor_repository

    def ajouter(self, vehicle):
        """Ajoute un véhicule au catalogue."""
        return self.vehicles.add(vehicle)

    def lister(self):
        """Retourne les véhicules du catalogue."""
        return self.vehicles.read_all()

    def chercher(self, vehicle_id):
        """Recherche un véhicule par son identifiant."""
        return self.vehicles.get_by_id(vehicle_id)

    def modifier(self, vehicle):
        """Mise à jour d'un véhicule du catalogue."""
        return self.vehicles.update(vehicle)

    def supprimer(self, vehicle_id):
        """Supprime un véhicule du catalogue."""
        return self.vehicles.delete(vehicle_id)

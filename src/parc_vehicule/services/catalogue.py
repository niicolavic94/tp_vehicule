"""Définit la couche service du catalogue des véhicules."""


class Catalogue:
    """Couche service qui centralise les opérations du catalogue."""

    def __init__(self, vehicle_repository, motor_repository=None):
        self.vehicles = vehicle_repository
        self.motors = motor_repository

    def ajouter(self, vehicle):
        return self.vehicles.add(vehicle)

    def lister(self):
        return self.vehicles.read_all()

    def chercher(self, vehicle_id):
        return self.vehicles.get_by_id(vehicle_id)

    def modifier(self, vehicle):
        return self.vehicles.update(vehicle)

    def supprimer(self, vehicle_id):
        return self.vehicles.delete(vehicle_id)

from projet_dev_avance.core.interfaces.AbstractVehiculeRepository import AbstractVehiculeRepository
from projet_dev_avance.core.interfaces.Vehicule import Vehicule

from repositories.abstractmotorrepository import AbstractMotorRepository


class InMemoryVehiculeRepository(AbstractVehiculeRepository):

    def __init__(self):
        self.__vehicles = []

    def create(self, vehicle: Vehicule):
        self.__vehicles.append(vehicle)

    def read(self):
        return self.__vehicles

    def update(self, updated_vehicle: Vehicule):
        for vehicle in self.__vehicles:
            if vehicle.id == updated_vehicle.id:
                vehicle = updated_vehicle

    def delete(self, vehicule_id: int):
        for vehicle in self.__vehicles:
            if vehicle.id == vehicule_id:
                del self.__vehicles[vehicle.id]


class InMemoryMotorRepository(AbstractMotorRepository):

    def __init__(self):
        self.__vehicles = []

    def create(self, vehicle: Vehicule):
        self.__vehicles.append(vehicle)

    def read(self):
        return self.__vehicles

    def update(self, updated_vehicle: Vehicule):
        for vehicle in self.__vehicles:
            if vehicle.id == updated_vehicle.id:
                vehicle = updated_vehicle

    def delete(self, vehicule_id: int):
        for vehicle in self.__vehicles:
            if vehicle.id == vehicule_id:
                del self.__vehicles[vehicle.id]
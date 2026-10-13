"""Dépôts de données."""

from parc_vehicule.repositories.memory_repository import MemoryRepository
from parc_vehicule.repositories.abstractmotorrepository import AbstractMotorRepository
from parc_vehicule.repositories.abstractvehiculerepository import AbstractVehicleRepository
from parc_vehicule.repositories.database_motor_repository import DatabaseMotorRepository
from parc_vehicule.repositories.database_vehicle_repository import DatabaseVehicleRepository
from parc_vehicule.repositories import mysql_connection

__all__ = [
    "MemoryRepository",
    "AbstractMotorRepository",
    "AbstractVehicleRepository",
    "DatabaseMotorRepository",
    "DatabaseVehicleRepository",
    "mysql_connection",
]

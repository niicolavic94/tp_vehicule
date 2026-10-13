"""Dépôts de données."""

from parc_vehicule.repositories.memory_repository import MemoryRepository
from parc_vehicule.repositories.database_motor_repository import DatabaseMotorRepository
from parc_vehicule.repositories.database_vehicle_repository import DatabaseVehicleRepository
from parc_vehicule.repositories import mysql_connection

__all__ = [
    "MemoryRepository",
    "DatabaseMotorRepository",
    "DatabaseVehicleRepository",
    "mysql_connection",
]

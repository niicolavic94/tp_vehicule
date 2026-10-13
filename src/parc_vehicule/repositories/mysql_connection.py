import os

from dotenv import load_dotenv
from parc_vehicule.database.database import engine  # utilise SQLAlchemy + pymysql

load_dotenv()


def get_connection():
    # Retourne une connexion raw compatible avec les repositories existants
    return engine.raw_connection()

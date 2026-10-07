import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            database="projet_dev_avance",
            user="root",
            password="root"
        )

        if connection.is_connected():
            print("Connexion MySQL réussie !")
            return connection

    except Error as e:
        print(f"Erreur de connexion MySQL : {e}")

    return None
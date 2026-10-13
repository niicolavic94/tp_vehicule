from parc_vehicule.repositories.mysql_connection import get_connection
from parc_vehicule.repositories.database_vehicle_repository import DatabaseVehicleRepository

conn = get_connection()
vehicules = DatabaseVehicleRepository(conn).read_all()
print(f"{'ID':<4} {'Marque':<12} {'Modèle':<12} {'Année':<6} {'Catégorie':<12} {'Moteur':<12} {'Autonomie':>10}")
print("-" * 70)
for v in vehicules:
    auto = f"{v.moteur.autonomie():.0f} km" if v.moteur else "N/A"
    print(f"{v.id:<4} {v.marque:<12} {v.modele:<12} {v.annee:<6} {v.categorie:<12} {v.moteur.type if v.moteur else 'N/A':<12} {auto:>10}")
conn.close()

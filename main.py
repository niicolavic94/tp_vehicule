from src.models.motorisations.thermique import Thermique
from src.models.motorisations.electrique import Electrique
from src.models.motorisations.hybride import Hybride

from src.models.vehicules.voiture import Voiture

from src.repositories.memory_repository import MemoryRepository


def main():

    # =========================
    # Création moteur thermique
    # =========================

    thermique = Thermique(
        reservoir_l=50,
        consommation_l_100km=5
    )

    print("===== MOTEUR THERMIQUE =====")
    print(thermique)
    print(f"Autonomie : {thermique.autonomie():.2f} km")
    print()


    # =========================
    # Création moteur électrique
    # =========================

    electrique = Electrique(
        capacite_kwh=75,
        consommation_kwh_100km=18
    )

    print("===== MOTEUR ELECTRIQUE =====")
    print(electrique)
    print(f"Autonomie : {electrique.autonomie():.2f} km")
    print()


    # =========================
    # Création moteur hybride
    # =========================

    hybride = Hybride(
        reservoir_l=45,
        consommation_l_100km=5,
        capacite_kwh=15,
        consommation_kwh_100km=15
    )

    print("===== MOTEUR HYBRIDE =====")
    print(hybride)
    print(
        f"Autonomie thermique : "
        f"{hybride.autonomie_thermique():.2f} km"
    )
    print(
        f"Autonomie électrique : "
        f"{hybride.autonomie_electrique():.2f} km"
    )
    print(
        f"Autonomie totale : "
        f"{hybride.autonomie():.2f} km"
    )
    print()


    # =========================
    # Création d'une voiture
    # =========================

    voiture = Voiture(
        marque="Toyota",
        modele="Prius",
        annee=2024,
        kilometrage=10000,
        volume_coffre=400,
        categorie="berline",
        moteur=hybride
    )

    print("===== VOITURE =====")
    print(voiture)
    print()


    # =========================
    # Repository mémoire
    # =========================

    repository = MemoryRepository()

    repository.add(voiture)

    print("===== REPOSITORY =====")

    print("Toutes les voitures :")
    print(repository.read_all())
    print()

    print("Voiture avec ID 1 :")
    print(repository.get_by_id(1))


if __name__ == "__main__":
    main()
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from parc_vehicule.core.exceptions import ValidationError
from parc_vehicule.core.interfaces import Motorisation
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.models.vehicules.voiture import Voiture
from parc_vehicule.repositories.mysql_connection import get_connection
from parc_vehicule.repositories.database_vehicle_repository import DatabaseVehicleRepository
from parc_vehicule.services.catalogue import Catalogue

router = APIRouter(prefix="/cars", tags=["cars"])


def get_service() -> Catalogue:
    conn = get_connection()
    return Catalogue(vehicle_repository=DatabaseVehicleRepository(conn))


# ---------- Schémas moteur ----------

class MoteurElectrique(BaseModel):
    type: Literal["electrique"]
    capacite_kwh: float
    consommation_kwh_100km: float


class MoteurThermique(BaseModel):
    type: Literal["thermique"]
    reservoir_l: float
    consommation_l_100km: float


class MoteurHybride(BaseModel):
    type: Literal["hybride"]
    reservoir_l: float
    consommation_l_100km: float
    capacite_kwh: float
    consommation_kwh_100km: float


# Le champ "type" sert à choisir le bon schéma
MoteurCreate = Annotated[
    MoteurElectrique | MoteurThermique | MoteurHybride,
    Field(discriminator="type"),
]


# ---------- Schémas voiture ----------

class VoitureCreate(BaseModel):
    """Corps du POST : pas d'id, il est attribué par le repository."""

    marque: str
    modele: str
    annee: int
    kilometrage: float
    volume_coffre: float
    categorie: str
    moteur: MoteurCreate


class VoitureRead(BaseModel):
    id: int
    marque: str
    modele: str
    annee: int
    kilometrage: float
    volume_coffre: float
    categorie: str
    moteur: str
    autonomie_km: float


# ---------- Conversions ----------

def creer_moteur(data) -> Motorisation:
    """Convertit le schéma reçu en objet Motorisation."""
    if isinstance(data, MoteurElectrique):
        return Electrique(data.capacite_kwh, data.consommation_kwh_100km)
    if isinstance(data, MoteurThermique):
        return Thermique(data.reservoir_l, data.consommation_l_100km)
    if isinstance(data, MoteurHybride):
        return Hybride(
            data.reservoir_l,
            data.consommation_l_100km,
            data.capacite_kwh,
            data.consommation_kwh_100km,
        )
    raise ValidationError(f"Moteur non géré : {data.type}")


def vers_read(voiture: Voiture) -> VoitureRead:
    return VoitureRead(
        id=voiture.id,
        marque=voiture.marque,
        modele=voiture.modele,
        annee=voiture.annee,
        kilometrage=voiture.kilometrage,
        volume_coffre=voiture.volume_coffre,
        categorie=voiture.categorie,
        moteur=voiture.moteur.type,
        autonomie_km=voiture.moteur.autonomie(),
    )


# ---------- Routes ----------

@router.get("/", response_model=list[VoitureRead])
async def index():
    return [vers_read(v) for v in get_service().lister()]


@router.get("/{car_id}", response_model=VoitureRead)
async def show(car_id: int):
    voiture = get_service().chercher(car_id)
    if voiture is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Véhicule introuvable")
    return vers_read(voiture)


@router.post("/", response_model=VoitureRead, status_code=status.HTTP_201_CREATED)
async def create(payload: VoitureCreate):
    try:
        voiture = Voiture(
            **payload.model_dump(exclude={"moteur"}),
            moteur=creer_moteur(payload.moteur),
        )
    except (ValidationError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))

    get_service().ajouter(voiture)
    return vers_read(voiture)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(car_id: int):
    if not get_service().supprimer(car_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Véhicule introuvable")
    


# AJOUT IA : modifier une voiture existante
@router.put("/{car_id}", response_model=VoitureRead)
async def update(car_id: int, payload: VoitureCreate):
    service = get_service()

    # AJOUT IA : vérifier que la voiture existe
    voiture_existante = service.chercher(car_id)
    if voiture_existante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable",
        )

    # AJOUT IA : reconstruire la voiture avec les nouvelles données
    try:
        voiture = Voiture(
            id=car_id,
            **payload.model_dump(exclude={"moteur"}),
            moteur=creer_moteur(payload.moteur),
        )
    except (ValidationError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # AJOUT IA : à relier à la méthode de modification
    # réellement disponible dans Catalogue / DatabaseVehicleRepository.
    # Exemple : service.modifier(car_id, voiture)
    raise NotImplementedError(
        "La méthode de modification du repository reste à implémenter."
    )



# AJOUT IA : consulter la motorisation d'une voiture
@router.get("/{car_id}/motorisations")
async def get_car_motorisation(car_id: int):
    voiture = get_service().chercher(car_id)

    if voiture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable",
        )

    # AJOUT IA : retourner les informations propres au moteur
    moteur = voiture.moteur

    if isinstance(moteur, Electrique):
        return {
            "type": "electrique",
            "capacite_kwh": moteur.capacite_kwh,
            "consommation_kwh_100km": moteur.consommation_kwh_100km,
            "autonomie_km": moteur.autonomie(),
        }

    if isinstance(moteur, Thermique):
        return {
            "type": "thermique",
            "reservoir_l": moteur.reservoir_l,
            "consommation_l_100km": moteur.consommation_l_100km,
            "autonomie_km": moteur.autonomie(),
        }

    if isinstance(moteur, Hybride):
        return {
            "type": "hybride",
            "reservoir_l": moteur.reservoir_l,
            "consommation_l_100km": moteur.consommation_l_100km,
            "capacite_kwh": moteur.capacite_kwh,
            "consommation_kwh_100km": moteur.consommation_kwh_100km,
            "autonomie_km": moteur.autonomie(),
        }

    # AJOUT IA : gestion d'un type de moteur non reconnu
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Type de motorisation non reconnu",
    )


# AJOUT IA : route PUT pour modifier une voiture existante
@router.put("/{car_id}", response_model=VoitureRead)
async def update(car_id: int, payload: VoitureCreate):
    service = get_service()

    # AJOUT IA : vérifier que la voiture existe
    voiture_existante = service.chercher(car_id)

    if voiture_existante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable",
        )

    # AJOUT IA : construire la voiture avec les données reçues
    try:
        voiture = Voiture(
            **payload.model_dump(exclude={"moteur"}),
            moteur=creer_moteur(payload.moteur),
            id=car_id,
        )
    except (ValidationError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # AJOUT IA : appeler la méthode modifier déjà présente dans Catalogue
    try:
        modifie = service.modifier(voiture)
    except (ValidationError, TypeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # AJOUT IA : gérer le cas où aucune ligne n'a été modifiée
    if not modifie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable ou non modifié",
        )

    # AJOUT IA : renvoyer la voiture au format de lecture
    return vers_read(voiture)


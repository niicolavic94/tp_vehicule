from typing import Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from parc_vehicule.core.exceptions import ValidationError
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.repositories.database_motor_repository import DatabaseMotorRepository
from parc_vehicule.repositories.database_vehicle_repository import DatabaseVehicleRepository  # MODIF 1 : import ajouté pour accéder aux voitures par motor_id
from parc_vehicule.repositories.mysql_connection import get_connection
from parc_vehicule.routers.cars import VoitureRead  # MODIF 2 : import du schéma de réponse VoitureRead depuis cars.py
from parc_vehicule.routers.cars import vers_read as vers_voiture_read  # MODIF 2 : import de la fonction de conversion, aliasée pour éviter le conflit avec vers_read local

# AJOUT IA : fichier complet — toutes les routes /motorisations sont nouvelles

router = APIRouter(prefix="/motorisations", tags=["motorisations"])


def get_repo() -> DatabaseMotorRepository:
    return DatabaseMotorRepository(get_connection())


# ---------- Schémas ----------

class MoteurThermiqueCreate(BaseModel):
    type: Literal["thermique"]
    reservoir_l: float
    consommation_l_100km: float
    power: float | None = None


class MoteurElectriqueCreate(BaseModel):
    type: Literal["electrique"]
    capacite_kwh: float
    consommation_kwh_100km: float
    power: float | None = None


class MoteurHybrideCreate(BaseModel):
    type: Literal["hybride"]
    reservoir_l: float
    consommation_l_100km: float
    capacite_kwh: float
    consommation_kwh_100km: float
    power: float | None = None


class MoteurRead(BaseModel):
    id: int
    type: str
    power: float | None
    autonomie_km: float


# ---------- Conversion ----------

def creer_moteur(data):
    kwargs = {"power": data.power} if data.power else {}
    if isinstance(data, MoteurThermiqueCreate):
        return Thermique(data.reservoir_l, data.consommation_l_100km, **kwargs)
    if isinstance(data, MoteurElectriqueCreate):
        return Electrique(data.capacite_kwh, data.consommation_kwh_100km, **kwargs)
    if isinstance(data, MoteurHybrideCreate):
        return Hybride(
            data.reservoir_l,
            data.consommation_l_100km,
            data.capacite_kwh,
            data.consommation_kwh_100km,
            **kwargs,
        )
    raise ValidationError(f"Type non géré : {data.type}")


def vers_read(moteur) -> MoteurRead:
    return MoteurRead(
        id=moteur.id,
        type=moteur.type,
        power=getattr(moteur, "power", None),
        autonomie_km=moteur.autonomie(),
    )


# ---------- Routes ----------

@router.get("/", response_model=list[MoteurRead])
async def index():
    return [vers_read(m) for m in get_repo().read_all()]


@router.post("/", response_model=MoteurRead, status_code=status.HTTP_201_CREATED)
async def create(payload: MoteurThermiqueCreate | MoteurElectriqueCreate | MoteurHybrideCreate):
    try:
        moteur = creer_moteur(payload)
    except (ValidationError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    get_repo().add(moteur)
    return vers_read(moteur)


@router.get("/{motorisation_id}", response_model=MoteurRead)
async def show(motorisation_id: int):
    moteur = get_repo().get_by_id(motorisation_id)
    if moteur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")
    return vers_read(moteur)


@router.put("/{motorisation_id}", response_model=MoteurRead)
async def update(
    motorisation_id: int,
    payload: MoteurThermiqueCreate | MoteurElectriqueCreate | MoteurHybrideCreate,
):
    repo = get_repo()
    if repo.get_by_id(motorisation_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")
    try:
        moteur = creer_moteur(payload)
        moteur.id = motorisation_id
    except (ValidationError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    repo.update(moteur)
    return vers_read(moteur)


@router.delete("/{motorisation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(motorisation_id: int):
    if not get_repo().delete(motorisation_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")


#BOOOOOOOOOOOOOOOOOONUS : route pour récupérer toutes les voitures d'une motorisation



@router.get("/{motorisation_id}/cars", response_model=list[VoitureRead])
async def get_cars(motorisation_id: int):
    moteur = get_repo().get_by_id(motorisation_id)

    if moteur is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorisation introuvable"
        )

    voitures = DatabaseVehicleRepository(get_connection()).get_by_motor_id(  # MODIF 3 : `connection` indéfini remplacé par get_connection()
        motorisation_id
    )

    return [vers_voiture_read(v) for v in voitures]

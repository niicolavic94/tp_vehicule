from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError

from parc_vehicule.core.exceptions import ValidationError
from parc_vehicule.database.database import get_db
from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.services.catalogue import Catalogue
from parc_vehicule.services.motor_catalogue import MotorCatalogue, MotorInUseError
from parc_vehicule.routers.cars import VoitureRead, vers_read as vers_voiture_read

router = APIRouter(prefix="/motorisations", tags=["motorisations"])


def get_service(session=Depends(get_db)) -> MotorCatalogue:
    return MotorCatalogue(session)


def get_vehicle_service(session=Depends(get_db)) -> Catalogue:
    return Catalogue(session)


# ---------- Schémas ----------

class MoteurThermiqueCreate(BaseModel):
    type: Literal["thermique"]
    reservoir_l: float
    consommation_l_100km: float
    power: float | None = Field(default=None, gt=0)


class MoteurElectriqueCreate(BaseModel):
    type: Literal["electrique"]
    capacite_kwh: float
    consommation_kwh_100km: float
    power: float | None = Field(default=None, gt=0)


class MoteurHybrideCreate(BaseModel):
    type: Literal["hybride"]
    reservoir_l: float
    consommation_l_100km: float
    capacite_kwh: float
    consommation_kwh_100km: float
    power: float | None = Field(default=None, gt=0)


class MoteurRead(BaseModel):
    id: int
    type: str
    power: float | None
    autonomie_km: float


# ---------- Conversion ----------

def creer_moteur(data):
    kwargs = {"power": data.power} if data.power is not None else {}
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
async def index(service: MotorCatalogue = Depends(get_service)):
    return [vers_read(m) for m in service.lister()]


@router.post("/", response_model=MoteurRead, status_code=status.HTTP_201_CREATED)
async def create(
    payload: MoteurThermiqueCreate | MoteurElectriqueCreate | MoteurHybrideCreate,
    service: MotorCatalogue = Depends(get_service),
):
    try:
        moteur = creer_moteur(payload)
    except (ValidationError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    service.ajouter(moteur)
    return vers_read(moteur)


@router.get("/{motorisation_id}", response_model=MoteurRead)
async def show(
    motorisation_id: int,
    service: MotorCatalogue = Depends(get_service),
):
    moteur = service.chercher(motorisation_id)
    if moteur is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")
    return vers_read(moteur)


@router.put("/{motorisation_id}", response_model=MoteurRead)
async def update(
    motorisation_id: int,
    payload: MoteurThermiqueCreate | MoteurElectriqueCreate | MoteurHybrideCreate,
    service: MotorCatalogue = Depends(get_service),
):
    if service.chercher(motorisation_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")
    try:
        moteur = creer_moteur(payload)
        moteur.id = motorisation_id
    except (ValidationError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    if not service.modifier(motorisation_id, moteur):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")
    return vers_read(moteur)


@router.delete("/{motorisation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    motorisation_id: int,
    service: MotorCatalogue = Depends(get_service),
):
    try:
        deleted = service.supprimer(motorisation_id)
    except MotorInUseError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    except IntegrityError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Cette motorisation est encore utilisée par un véhicule",
        ) from e
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Motorisation introuvable")


#BOOOOOOOOOOOOOOOOOONUS : route pour récupérer toutes les voitures d'une motorisation



@router.get("/{motorisation_id}/cars", response_model=list[VoitureRead])
async def get_cars(
    motorisation_id: int,
    service: MotorCatalogue = Depends(get_service),
    vehicle_service: Catalogue = Depends(get_vehicle_service),
):
    moteur = service.chercher(motorisation_id)

    if moteur is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorisation introuvable"
        )

    voitures = vehicle_service.lister_par_motorisation(motorisation_id)

    return [vers_voiture_read(v) for v in voitures]

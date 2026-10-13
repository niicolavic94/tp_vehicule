from parc_vehicule.core import ValidationError


def valider_texte(valeur: str, nom: str) -> str:
    if not isinstance(valeur, str) or not valeur.strip():
        raise ValidationError(
            f"{nom} doit être un texte non vide."
        )

    return valeur.strip()


def valider_positif(valeur: float, nom: str) -> float:
    if not isinstance(valeur, (int, float)) or valeur <= 0:
        raise ValidationError(
            f"{nom} doit être strictement positif."
        )

    return valeur


def valider_positif_ou_nul(valeur: float, nom: str) -> float:
    if not isinstance(valeur, (int, float)) or valeur < 0:
        raise ValidationError(
            f"{nom} doit être positif ou nul."
        )

    return valeur


def valider_annee(valeur: int) -> int:
    if not isinstance(valeur, int):
        raise ValidationError(
            "L'année doit être un entier."
        )

    if valeur < 1886:
        raise ValidationError(
            "L'année doit être supérieure ou égale à 1886."
        )

    return valeur
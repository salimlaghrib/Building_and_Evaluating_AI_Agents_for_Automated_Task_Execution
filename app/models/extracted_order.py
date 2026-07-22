from typing import Optional

from pydantic import BaseModel, Field


class ExtractedOrder(BaseModel):
    client_name: Optional[str] = Field(
        None,
        description="Nom du client"
    )

    product: Optional[str] = Field(
        None,
        description="Type de produit (matelas, sommier, etc.)"
    )

    length: Optional[float] = Field(
        None,
        description="Longueur en cm",
        ge=0
    )

    width: Optional[float] = Field(
        None,
        description="Largeur en cm",
        ge=0
    )

    height: Optional[float] = Field(
        None,
        description="Hauteur en cm",
        ge=0
    )

    quantity: Optional[int] = Field(
        1,
        description="Quantité demandée",
        ge=1
    )

    observations: Optional[str] = Field(
        None,
        description="Informations complémentaires extraites du dessin ou du message"
    )

    confidence: Optional[float] = Field(
        None,
        description="Niveau de confiance de l'extraction (0 à 1)",
        ge=0.0,
        le=1.0
    )
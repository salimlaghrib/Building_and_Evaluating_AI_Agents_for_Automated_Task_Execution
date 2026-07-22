from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderMessage(BaseModel):
    source: str = Field(
        ...,
        description="Source du message (WhatsApp, Gmail, etc.)"
    )

    phone: Optional[str] = Field(
        default=None,
        description="Numéro de téléphone du client"
    )

    email: Optional[str] = Field(
        default=None,
        description="Adresse email du client"
    )

    sender_name: Optional[str] = Field(
        default=None,
        description="Nom de l'expéditeur"
    )

    subject: Optional[str] = Field(
        default=None,
        description="Sujet de l'email (uniquement pour Gmail)"
    )

    message_text:Optional[str] =Field(
        default=None,
        description="Texte envoyé par le client"
    )

    image_path: str = Field(
        ...,
        description="Chemin local de l'image reçue"
    )

    timestamp: datetime = Field(
        ...,
        description="Date et heure de réception du message"
    )
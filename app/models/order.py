from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel,EmailStr,Field

class OrderStatus(str,Enum):
    PENDING = "PENDING"
    READY_FOR_VALIDATION = "READY_FOR_VALIDATION"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
class Order(BaseModel):
    
    # Informations du client
    client_name: str
    phone: str | None = None
    email: EmailStr | None = None
    # address: str
    # Informations du produit
    product: Optional[str] = Field(default="Matelas")

    # Dimensions (cm)
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)

    # Quantité
    quantity: int = Field(..., ge=1)

    # Informations de suivi
    status: OrderStatus = OrderStatus.PENDING
    validation_required: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
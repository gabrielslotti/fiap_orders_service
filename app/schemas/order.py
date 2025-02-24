from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, ConfigDict


class OrderStatusEnum(str, Enum):
    received = "Recebido"
    preparing = "Em preparação"
    done = "Pronto"
    finished = "Finalizado"


class OrderCheckout(BaseModel):
    customer_id: int | None
    items: List[Dict]


class OrderCreate(BaseModel):
    external_id: str


class OrderCreateResponse(BaseModel):
    """Order Schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    mongo_id: str
    customer_id: int
    status: OrderStatusEnum
    items: List[Dict]
    price: float


class OrderUpdate(BaseModel):
    external_id: str
    status: OrderStatusEnum


class OrderUpdateResponse(BaseModel):
    id: int
    status: OrderStatusEnum


class OrderCheckoutResponse(BaseModel):
    external_id: str
    status: str
    value: float
    qrcode: str

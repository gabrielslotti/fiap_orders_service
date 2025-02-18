from pydantic import BaseModel, ConfigDict
from typing import List, Dict
from enum import Enum


class OrderStatusEnum(str, Enum):
    received = 'Recebido'
    preparing = 'Em preparação'
    done = 'Pronto'
    finished = 'Finalizado'


class OrderCreate(BaseModel):
    customer_id: int | None
    items: List[Dict]


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
    id: int
    status: OrderStatusEnum

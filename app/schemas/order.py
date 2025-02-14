from pydantic import BaseModel, ConfigDict
from enum import Enum


class OrderStatusEnum(str, Enum):
    received = 'Recebido'
    preparing = 'Em preparação'
    done = 'Pronto'
    finished = 'Finalizado'


class OrderBase(BaseModel):
    """Order Base Schema."""
    customer_id: int | None
    status: OrderStatusEnum
    # items: Dict


class OrderCreate(OrderBase):
    ...


class OrderUpdate(BaseModel):
    id: int
    status: OrderStatusEnum


class Order(OrderBase):
    """Order Schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int | None

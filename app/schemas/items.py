from pydantic import BaseModel, ConfigDict
from enum import Enum


class ItemCategoryEnum(str, Enum):
    """Item Category Enum."""
    lanche = 'Lanche'
    acompanhamento = 'Acompanhamento'
    bebida = 'Bebida'
    sobremesa = 'Sobremesa'


class ItemBase(BaseModel):
    """Item Base Schema."""
    title: str
    description: str
    category: ItemCategoryEnum
    amount: int
    price: float


class ItemRegister(ItemBase):
    ...


class Item(ItemBase):
    """Item Schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int

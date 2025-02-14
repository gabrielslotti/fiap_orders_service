from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    """Customer Base Schema."""

    cpf: str
    first_name: str
    last_name: str
    email: str


class CustomerRegister(CustomerBase):
    ...


class CustomerIdentify(BaseModel):
    cpf: str


class Customer(CustomerBase):
    """Customer Schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int | None

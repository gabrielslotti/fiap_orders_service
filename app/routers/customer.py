from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.main import logger
from app.models.customer import Customer as CustomerModel
from app.schemas.customer import Customer, CustomerIdentify, CustomerRegister
from app.schemas.http import DefaultResponse

from .. import database

router = APIRouter()


@router.post(
    "/register", response_model=DefaultResponse, status_code=status.HTTP_201_CREATED
)
def register_customer(
    customer: CustomerRegister, db_session: Session = Depends(database.get_db)
):
    """
    Regiser a new customer.

    :param customer: Customer schema.
    :param db_session: Database session.
    """
    db_customer = CustomerModel(**customer.model_dump())
    db_session.add(db_customer)
    db_session.commit()
    db_session.refresh(db_customer)

    logger.debug(f"Customer {db_customer.cpf} registered")

    return {"detail": f"Customer {db_customer.cpf} registered"}


@router.post("/identify", response_model=Customer)
def identify_customer(
    identity: CustomerIdentify, db_session: Session = Depends(database.get_db)
):
    """
    Get customer data by its CPF.

    :param identity: CustomerIdentify schema (cpf).
    :param db_session: Database session.
    """
    customer = (
        db_session.query(CustomerModel)
        .filter(CustomerModel.cpf == identity.cpf)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not registered"
        )

    return customer

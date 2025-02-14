from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.customer import Customer as CustomerModel
from app.schemas.customer import Customer, CustomerRegister, CustomerIdentify
from app.schemas.http import DefaultResponse
from app.main import logger
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
    try:
        db_customer = CustomerModel(**customer.model_dump())
        db_session.add(db_customer)
        db_session.commit()
        db_session.refresh(db_customer)

        logger.debug(f"Customer {db_customer.cpf} registered")

        return {"detail": f"Customer {db_customer.cpf} registered"}

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(status_code=500, detail="Database operation failed")


@router.post("/identify", response_model=Customer)
def identify_customer(
    identity: CustomerIdentify, db_session: Session = Depends(database.get_db)
):
    """
    Get customer data by its CPF.

    :param identity: CustomerIdentify schema (cpf).
    :param db_session: Database session.
    """
    try:
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

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

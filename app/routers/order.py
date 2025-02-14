from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.order import Order as OrderModel, OrderStatus as OrderStatusModel
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.main import logger
from .. import database


router = APIRouter()


@router.post(
    "/create", response_model=Order, status_code=status.HTTP_201_CREATED
)
def register_order(
    order: OrderCreate, db_session: Session = Depends(database.get_db)
):
    """
    Create a new order.

    :param order: Order schema.
    :param db_session: Database session.
    """
    try:
        order_raw = order.model_dump()

        # Get item category id
        order_status = (
            db_session.query(OrderStatusModel)
            .filter(OrderStatusModel.description == order_raw["status"])
            .one_or_none()
        )

        order_raw["status"] = order_status.id

        db_order = OrderModel(**order_raw)
        db_session.add(db_order)
        db_session.commit()
        db_session.refresh(db_order)

        logger.debug(f"Order {db_order.id} created")

        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            status=status.description
        )

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(status_code=500, detail="Database operation failed")


@router.post("/update", response_model=Order)
def update_order(
    order: OrderUpdate, db_session: Session = Depends(database.get_db)
):
    """
    Update Order status.

    :param order: Order update schema.
    :param db_session: Database session.
    """
    try:
        db_order = (
            db_session.query(OrderModel).filter(OrderModel.id == order.id).one_or_none()
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order does not exist"
            )

        # Get item category id
        order_status = (
            db_session.query(OrderStatusModel)
            .filter(OrderStatusModel.description == order.status)
            .one_or_none()
        )

        db_order.status = order_status.id

        db_session.add(db_order)
        db_session.commit()
        db_session.refresh(db_order)

        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            status=status.description
        )

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

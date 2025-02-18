from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.order import (
    Order as OrderModel,
    OrderStatus as OrderStatusModel,
)
from app.schemas.order import OrderCreate, OrderCreateResponse, OrderUpdate
from app.main import logger
from .. import database


router = APIRouter()


@router.post(
    "/create", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED
)
def register_order(
    order: OrderCreate, request: Request, db_session: Session = Depends(database.get_db)
):
    """
    Create a new order.

    :param order: Order schema.
    :param db_session: Database session.
    """
    try:
        order_raw = order.model_dump()

        # Create order cart on mongo db
        order_id = request.app.mongo.db.orders_cart.insert_one(order_raw).inserted_id

        # Get final price
        final_price = 0.0
        items = order_raw["items"]
        for item in items:
            final_price += item["price"]

        # Get item category id
        order_status = (
            db_session.query(OrderStatusModel)
            .filter(OrderStatusModel.description == "Recebido")
            .one_or_none()
        )

        order_raw["status"] = order_status.id
        order_raw["mongo_id"] = str(order_id)  # cart id
        del order_raw["items"]
        del order_raw["_id"]

        db_order = OrderModel(**order_raw)
        db_session.add(db_order)
        db_session.commit()
        db_session.refresh(db_order)

        # Build response
        response = OrderCreateResponse(
            id=db_order.id,
            mongo_id=db_order.mongo_id,
            customer_id=db_order.customer_id,
            status=order_status.description,
            items=items,
            price=final_price,
        )

        # Post message on RabbitMQ
        request.app.pika_client.send_message(response.model_dump())

        logger.debug(f"Order {db_order.mongo_id} created")

        return response

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(status_code=500, detail="Database operation failed")


@router.post("/update", response_model=OrderUpdate)
def update_order(order: OrderUpdate, db_session: Session = Depends(database.get_db)):
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

        return OrderUpdate(id=db_order.id, status=status.description)

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

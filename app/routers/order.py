from functools import lru_cache

import httpx
from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.main import logger
from app.models.order import Order as OrderModel
from app.models.order import OrderStatus as OrderStatusModel
from app.schemas.order import (
    OrderCheckout,
    OrderCheckoutResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderUpdate,
    OrderUpdateResponse,
)

from .. import config, database


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

router = APIRouter()


@router.post(
    "/checkout",
    response_model=OrderCheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def checkout(
    order: OrderCheckout,
    request: Request,
    db_session: Session = Depends(database.get_db),
):
    """
    Checkout the cart with items.

    :param order: Order checkout schema.
    :param db_session: Database session.
    """
    order_raw = order.model_dump()

    # Get final price
    final_price = 0.0
    items = order_raw["items"]
    for item in items:
        final_price += item["price"] * item["amount"]

    order_raw["total"] = final_price

    # Create order cart on mongo db
    order_id = request.app.mongo.db.orders_cart.insert_one(order_raw).inserted_id

    # Call payment service to generate QRCode
    req = httpx.post(
        f"{conf_settings.payment_service_url}/qrcode",
        json={"external_id": str(order_id), "value": final_price},
    )

    logger.debug(f"Checking out cart {str(order_id)}")

    return OrderCheckoutResponse(**req.json())


@router.post(
    "/create", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED
)
def register_order(
    checkout: OrderCreate,
    request: Request,
    db_session: Session = Depends(database.get_db),
):
    """
    Create a new order.

    :param order: Order schema.
    :param db_session: Database session.
    """
    checkout = checkout.model_dump()

    # Get order cart on mongo db
    order = request.app.mongo.db.orders_cart.find_one(
        {"_id": ObjectId(checkout["external_id"])}
    )

    if not order:
        logger.error(f"Order {checkout['external_id']} not found on MongoDB!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Get item category id
    order_status = (
        db_session.query(OrderStatusModel)
        .filter(OrderStatusModel.description == "Recebido")
        .one_or_none()
    )

    db_order = OrderModel(
        mongo_id=checkout["external_id"],
        customer_id=order["customer_id"],
        status=order_status.id,
    )
    db_session.add(db_order)
    db_session.commit()
    db_session.refresh(db_order)

    # Post message on RabbitMQ
    request.app.pika_client.send_message(
        {
            "id": db_order.id,
            "external_id": db_order.mongo_id,
            "status": order_status.description,
            "items": order["items"],
        }
    )

    logger.debug(f"Order {db_order.mongo_id} created")

    return OrderCreateResponse(
        id=db_order.id,
        mongo_id=db_order.mongo_id,
        customer_id=db_order.customer_id,
        status=order_status.description,
        items=order["items"],
        price=order["total"],
    )


@router.post("/update", response_model=OrderUpdateResponse)
def update_order(order: OrderUpdate, db_session: Session = Depends(database.get_db)):
    """
    Update Order status.

    :param order: Order update schema.
    :param db_session: Database session.
    """
    db_order = (
        db_session.query(OrderModel)
        .filter(OrderModel.mongo_id == order.external_id)
        .one_or_none()
    )

    if not db_order:
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

    return OrderUpdateResponse(id=db_order.id, status=order_status.description)

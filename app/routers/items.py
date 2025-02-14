from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.models.items import (
    Items as ItemsModel,
    ItemsCategory as ItemsCategoryModel,
)
from app.schemas.items import Item, ItemRegister, ItemCategoryEnum
from app.schemas.http import DefaultResponse
from app.main import logger
from .. import database


router = APIRouter()


@router.post("/register", response_model=Item, status_code=status.HTTP_201_CREATED)
def register_item(item: ItemRegister, db_session: Session = Depends(database.get_db)):
    """
    Register a new menu item.

    :param item: Item schema.
    :param db_session: Database session.
    """
    try:
        item_raw = item.model_dump()

        # Get item category id
        category = (
            db_session.query(ItemsCategoryModel)
            .filter(ItemsCategoryModel.description == item_raw["category"])
            .one_or_none()
        )

        item_raw["category"] = category.id

        db_item = ItemsModel(**item_raw)
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        logger.debug(f"Menu item {db_item.title} registered")

        return Item(
            id=db_item.id,
            title=db_item.title,
            description=db_item.description,
            category=category.description,
            amount=db_item.amount,
            price=db_item.price,
        )

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(status_code=500, detail="Database operation failed")


@router.put("/update", response_model=Item)
def update_item(item: Item, db_session: Session = Depends(database.get_db)):
    """
    Update a menu item.

    :param item: Item schema.
    :param db_session: Database session.
    """
    try:
        db_item = (
            db_session.query(ItemsModel).filter(ItemsModel.id == item.id).one_or_none()
        )

        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        category = (
            db_session.query(ItemsCategoryModel)
            .filter(ItemsCategoryModel.description == item.category)
            .one_or_none()
        )

        db_item.title = item.title
        db_item.description = item.description
        db_item.amount = item.amount
        db_item.price = item.price
        db_item.category = category.id

        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        logger.debug(f"Menu item {db_item.title} updated")

        return Item(
            id=db_item.id,
            title=db_item.title,
            description=db_item.description,
            category=category.description,
            amount=db_item.amount,
            price=db_item.price,
        )

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router.delete("/delete/{item_id}", response_model=DefaultResponse)
def delete_item(item_id: int, db_session: Session = Depends(database.get_db)):
    """
    Get items data by its CPF.

    :param identity: ItemsIdentify schema (cpf).
    :param db_session: Database session.
    """
    try:
        db_item = (
            db_session.query(ItemsModel).filter(ItemsModel.id == item_id).one_or_none()
        )

        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        db_session.delete(db_item)
        db_session.commit()

        return {"detail": f"Item {db_item.title} deleted"}

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router.get("/list/{category}", response_model=List[Item])
def list_items_by_category(
    category: ItemCategoryEnum, db_session: Session = Depends(database.get_db)
):
    """
    Get items data by its CPF.

    :param category: Item Category.
    :param db_session: Database session.
    """
    try:
        items = (
            db_session.query(ItemsModel)
            .with_entities(
                ItemsModel.id,
                ItemsModel.title,
                ItemsModel.description,
                ItemsModel.amount,
                ItemsModel.price,
                ItemsCategoryModel.description.label("category"),
            )
            .join(ItemsCategoryModel)
            .filter(ItemsCategoryModel.description == category)
            .all()
        )

        return items

    except SQLAlchemyError as exc:
        logger.exception(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

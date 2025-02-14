from sqlalchemy import ForeignKey, Integer, Float, Text, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ItemsCategory(Base):
    __tablename__ = 'items_category'

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    description: Mapped[String(40)] = mapped_column(type_=String(40), nullable=False)  # noqa


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    title: Mapped[String(120)] = mapped_column(type_=String(120), nullable=False)  # noqa
    description: Mapped[Text()] = mapped_column(type_=Text(), nullable=False)
    category: Mapped[Integer] = mapped_column(ForeignKey("items_category.id"))
    amount: Mapped[Integer] = mapped_column(type_=Integer, nullable=False)
    price: Mapped[Float] = mapped_column(type_=Float, nullable=False)

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class OrderStatus(Base):
    __tablename__ = 'order_status'

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    description: Mapped[String(20)] = mapped_column(type_=String(20), nullable=False)  # noqa


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    mongo_id: Mapped[String(120)] = mapped_column(type_=String(120))
    customer_id: Mapped[Integer] = mapped_column(type_=Integer, nullable=True)
    status: Mapped[Integer] = mapped_column(ForeignKey("order_status.id"))
    # items: Mapped[JSONB] = mapped_column(type_=JSONB, nullable=False)

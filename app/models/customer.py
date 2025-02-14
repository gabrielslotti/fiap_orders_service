from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    cpf: Mapped[String(11)] = mapped_column(type_=String(11), nullable=False)
    first_name: Mapped[String(60)] = mapped_column(type_=String(60), nullable=False)  # noqa
    last_name: Mapped[String(60)] = mapped_column(type_=String(60), nullable=False)  # noqa
    email: Mapped[String(120)] = mapped_column(type_=String(120), nullable=False)  # noqa

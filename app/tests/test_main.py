import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app import main
from app.tests.db import engine, override_get_db


@pytest.fixture()
def test_db():
    """
    Test database.
    """
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO items_category (description) "
            "VALUES ('Lanche'), ('Acompanhamento'), ('Bebida'), ('Sobremesa')"
        ))
        conn.commit()

    yield
    Base.metadata.drop_all(bind=engine)


main.app.dependency_overrides[get_db] = override_get_db

client = TestClient(main.app)


def test_health():
    """
    Test health route.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_customer(test_db):
    response = client.post(
        "/customer/register",
        json={
            "cpf": "10634272829",
            "first_name": "Jorge",
            "last_name": "Sousa",
            "email": "jorge.sousa@outlook.com"
        }
    )

    assert response.status_code == 201
    assert response.json() == {"detail": "Customer 10634272829 registered"}

    response = client.post(
        "/customer/identify",
        json={"cpf": "10634272829"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "cpf": "10634272829",
        "first_name": "Jorge",
        "last_name": "Sousa",
        "email": "jorge.sousa@outlook.com",
        "id": 1
    }


def test_identify_non_existing_customer(test_db):
    """Identify non existing customer"""

    response = client.post(
        "/customer/identify",
        json={"cpf": "10634272829"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not registered"
    }


def test_item(test_db):
    response = client.post(
        "/items/register",
        json={
            "title": "X-Egg",
            "description": "Lanche feito com pão de gergelim, hamburguer de 150g de costela, alface, tomate, queijo, ovo frito e maionese da casa.",
            "category": "Lanche",
            "amount": 1,
            "price": 32.0
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "title": "X-Egg",
        "description": "Lanche feito com pão de gergelim, hamburguer de 150g de costela, alface, tomate, queijo, ovo frito e maionese da casa.",
        "category": "Lanche",
        "amount": 1,
        "price": 32.0,
        "id": 1
    }

    response = client.put(
        "/items/update",
        json={
            "title": "X-Egg 2.0",
            "description": "Lanche feito com pão de gergelim, hamburguer de 150g de costela, alface, tomate, queijo, ovo frito e maionese da casa.",
            "category": "Lanche",
            "amount": 10,
            "price": 25.0,
            "id": 1
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "X-Egg 2.0",
        "description": "Lanche feito com pão de gergelim, hamburguer de 150g de costela, alface, tomate, queijo, ovo frito e maionese da casa.",
        "category": "Lanche",
        "amount": 10,
        "price": 25.0,
        "id": 1
    }

    response = client.get("/items/list/Lanche")

    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "X-Egg 2.0",
            "description": "Lanche feito com pão de gergelim, hamburguer de 150g de costela, alface, tomate, queijo, ovo frito e maionese da casa.",
            "category": "Lanche",
            "amount": 10,
            "price": 25.0,
            "id": 1
        }
    ]

    response = client.delete("/items/delete/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Item X-Egg 2.0 deleted"}

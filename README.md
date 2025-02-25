[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gabrielslotti_fiap_orders_service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=gabrielslotti_fiap_orders_service)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=gabrielslotti_fiap_orders_service&metric=coverage)](https://sonarcloud.io/summary/new_code?id=gabrielslotti_fiap_orders_service)

## Desenho da Arquitetura
![image](https://github.com/user-attachments/assets/b483ef6f-5cad-42a5-807d-e3b0a7d039d2)


## Vídeos
[Explicação da Arquitetura, Testes e Deploy](https://youtu.be/iFhyxGboZ6o)

[Demonstração do Funcionamento da Aplicação](https://youtu.be/qgGzgluKPw8)

## Tecnologias Usadas

- **Python**: Linguagem de programação principal.
- **FastAPI**: Framework para construção de APIs.
- **UV**: Ferramenta para gerenciamento de dependências.
- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional.
- **MongoDB**: Banco de dados não-relacional (NoSQL).
- **RabbitMQ**: Broker de mensageria.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Alembic**: Ferramenta para migrações de banco de dados.
- **Uvicorn**: ASGI Web Server.

## Estrutura do Projeto

A estrutura básica do projeto é organizada da seguinte maneira:

```
food_orders_service
├── alembic/
├── alembic.ini
├── app
│   ├── models/
│   ├── schemas/
│   └── routers/
│   └── tests/
│   └── main.py
│   └── settings.py
│   └── database.py
│   └── mongo.py
│   └── pika.py
```

Entendendo melhor o que é cada uma das pastas e arquivos:

- `models/`: Aqui contém todos os models das nossas entidades no banco de dados.
- `routers/`: Aqui contém os endpoints da nossa API, onde acontece toda a mágica.
- `schemas/`: Aqui contém todos schemas para validar os inputs e outputs nos nossos routers.
- `tests/`: Aqui contém todos os nossos testes (unitários, integração e comportamento).
- `*.py`: Os arquivos .py são arquivos com a implementação dos nossos clients para interagir com as ferramentas externas que estamos utilizando: Postgres, Mongo e RabbitMQ. Sendo o `settings.py` nosso arquivo com as configs do projeto e o `main.py` onde instânciamos nosso app para ser executado com `uvicorn`.


## Instalação e uso (local)

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/gabrielslotti/fiap_orders_service.git
    cd fiap_orders_service
    ```

2. **Instale o UV:**

    Siga as instruções da [documentação oficial do UV para instalação da ferramenta](https://docs.astral.sh/uv/getting-started/installation/). Mas para exemplo utilizando o `pip` podemos executar o seguinte comando:
    ```bash
    pip install uv
    ```

2. **Crie e ative um ambiente virtual (opcional)**:
    ```bash
    uv venv
    ```

3. **Instale as dependências (opcional)**:

    ```bash
    uv sync
    ```

    Opcional, pois ao rodar o projeto com uv as dependências já serão instaladas.

4. **Aplique as migrações**:

    ```bash
    uv run alembic upgrade head
    ```

    Importante ter o banco de dados (PostgreSQL) rodando com o banco que será utilizado criado.

5. **Configurar variáveis de ambiente:**

    Crie um arquivo `.env` na raíz do projeto e adicione as seguintes variáveis (caso não forneça o projeto utilizará os valores default no `app/configs.py`):

    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASS=postgres
    DB_BASE=food
    RABBIT_HOST=localhost
    RABBIT_PORT=5672
    RABBIT_USER=admin
    RABBIT_PASS=admin
    PUBLISH_QUEUE=food_orders
    MONGO_HOST=localhost
    MONGO_PORT=27017
    MONGO_USER=admin
    MONGO_PASS=admin
    MONGO_BASE=food_orders
    PAYMENT_SERVICE_URL=http://localhost:8001
    ```


6. **Inicie o app FastAPI com Uvicorn**:

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    O servidor estará rodando em `http://localhost:8000`.

7. **Acesse a documentação da API**:

    Acesse a documentação (Swagger) da API em `http://localhost:8000/docs`.


## Instalação e uso (docker)

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/gabrielslotti/fiap_orders_service.git
    cd fiap_orders_service
    ```

1. **Execute o docker compose**:

    ```bash
    docker compose up -d
    ```

    Este comando irá subir os containers do PostgreSQL, MongoDB, RabbitMQ e o app do projeto.

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8000

    # quantity of workers for uvicorn
    workers_count: int = 1

    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    env: str = "dev"
    debug: bool = True

    # Variables for RabbitMQ
    publish_queue: str = "food_orders"
    rabbit_host: str = "127.0.0.1"
    rabbit_user: str = "admin"
    rabbit_pass: str = "admin"

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = "postgres"
    db_base: str = "food"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    mongo_host: str = "127.0.0.1"
    mongo_port: int = 27017
    mongo_user: str = "admin"
    mongo_pass: str = "admin"
    mongo_base: str = "food_orders"

    @property
    def mongo_url(self) -> URL:
        return URL.build(
            scheme="mongodb",
            host=self.mongo_host,
            port=self.mongo_port,
            user=self.mongo_user,
            password=self.mongo_pass,
        )

    payment_service_url: str = "http://0.0.0.0:8001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

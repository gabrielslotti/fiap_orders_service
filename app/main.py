# import asyncio
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.mongo import Mongo
from app.pika import PikaClient
from app.routers import customer, items, order

from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()


class FoodOrdersApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient()
        self.mongo = Mongo()


app = FoodOrdersApp(debug=conf_settings.debug)

app.add_middleware(CORSMiddleware)

app.include_router(customer.router, prefix="/customer")
app.include_router(items.router, prefix="/items")
app.include_router(order.router, prefix="/order")

logger.add("log_api.log", rotation="100 MB")  # Automatically rotate log file


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed"},
    )


@app.get("/health")
def health():
    """
    Health router.
    """
    result = {"status": "ok"}
    return result

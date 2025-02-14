from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.routers import customer, items, order
from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

app = FastAPI(debug=conf_settings.debug)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=conf_settings.ALLOWED_ORIGINS,
    # allow_credentials=conf_settings.ALLOW_CREDENTIALS,
    # allow_methods=conf_settings.ALLOW_METHODS,
    # allow_headers=conf_settings.ALLOW_HEADERS,
)

app.include_router(customer.router, prefix="/customer")
app.include_router(items.router, prefix="/items")
app.include_router(order.router, prefix="/order")


logger.add("log_api.log", rotation="100 MB")  # Automatically rotate log file


@app.get("/health")
def health():
    """
    Health router.
    """
    result = {
        "status": "ok"
    }
    return result

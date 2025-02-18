from pymongo import MongoClient
from functools import lru_cache
from app.main import logger
from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

MONGODB_URL = str(conf_settings.mongo_url)


class Mongo():

    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        self.db = self.client[conf_settings.mongo_base]

        logger.info("MongoDB connection initialized")

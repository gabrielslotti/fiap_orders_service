import json
import uuid
from functools import lru_cache

import pika

from app.main import logger

from . import config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()


class PikaClient:

    def __init__(self):
        self.publish_queue_name = conf_settings.publish_queue

        self.connection = None
        self.channel = None
        self.publish_queue = None
        self.callback_queue = None
        # self.response = None

        logger.info("Pika connection initialized")

    def _connect(self):
        credentials = pika.PlainCredentials(
            conf_settings.rabbit_user, conf_settings.rabbit_pass
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=conf_settings.rabbit_host, credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(
            queue=self.publish_queue_name
        )  # noqa
        self.callback_queue = self.publish_queue.method.queue

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        if not self.connection:
            self._connect()

        self.channel.basic_publish(
            exchange="",
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message),
        )
        logger.debug(f"[RMQ] Publish: {message}")

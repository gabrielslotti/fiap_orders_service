import pika
import uuid
import json
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


class PikaClient:

    def __init__(self, process_callable=None):
        self.publish_queue_name = conf_settings.publish_queue

        credentials = pika.PlainCredentials(
            conf_settings.rabbit_user,
            conf_settings.rabbit_pass
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=conf_settings.rabbit_host,
                credentials=credentials
            )
        )

        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)  # noqa
        self.callback_queue = self.publish_queue.method.queue
        self.response = None

        if process_callable:
            self.process_callable = process_callable

        logger.info('Pika connection initialized')

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
        logger.debug(f"[RMQ] Publish: {message}")

import asyncio
import aio_pika
import logging
from consumer_messages.config.settings import settings


class BaseConsumer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.rabbitmq_url = settings.rabbitmq_connection_url

    async def handle_message(self, message: aio_pika.IncomingMessage):
        """Override this method in subclasses to define message handling."""
        raise NotImplementedError("Subclasses must implement this method")

    async def start(self):
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, durable=True, passive=True)

            logging.info(f"Waiting for messages on queue: {self.queue_name}")
            await queue.consume(self.handle_message)

            await asyncio.Future()  # Keep the consumer running
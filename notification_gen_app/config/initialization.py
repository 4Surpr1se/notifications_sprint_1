import asyncio
import logging

import aio_pika

from notification_gen_app.config.settings import settings


async def initialize_rabbitmq():
    # Set up an asynchronous connection to RabbitMQ
    connection = await aio_pika.connect_robust(settings.rabbitmq_connection_url)
    async with connection:
        # Open a channel
        channel = await connection.channel()

        # Declare the dead-letter exchange
        await channel.declare_exchange(settings.dlx_exchange, aio_pika.ExchangeType.DIRECT)

        # Define the primary queues and their DLQs
        # instant_message_queue = await channel.declare_queue(settings.instant_message_queue, passive=True)
        # await instant_message_queue.delete()

        # Instant Message Queue and DLQ
        instant_dlq = await channel.declare_queue(settings.instant_dlq, durable=True)
        instant_message_queue = await channel.declare_queue(
            settings.instant_message_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.instant_dlq
            }
        )

        # Scheduled Message Queue and DLQ
        scheduled_dlq = await channel.declare_queue(settings.scheduled_dlq, durable=True)
        scheduled_message_queue = await channel.declare_queue(
            settings.scheduled_message_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.scheduled_dlq
            }
        )

        # Bind DLQs to the dead-letter exchange
        await instant_dlq.bind(exchange=settings.dlx_exchange, routing_key=settings.instant_dlq)
        await scheduled_dlq.bind(exchange=settings.dlx_exchange, routing_key=settings.scheduled_dlq)

        # Define notification queues for the second worker

        # Instant Notification Queue (for messages that have been sent)
        await channel.declare_queue(settings.instant_notification_queue, durable=True)

        # Scheduled Notification Queue (for messages that have been sent)
        await channel.declare_queue(settings.scheduled_notification_queue, durable=True)

        logging.info("RabbitMQ initialization complete.")
        print("RabbitMQ initialization complete.")


# Example of running the initialization asynchronously
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(initialize_rabbitmq())

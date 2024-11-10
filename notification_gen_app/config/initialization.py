import asyncio
import logging

import aio_pika

from notification_gen_app.config.settings import settings


# TODO x-retry-count
async def initialize_rabbitmq():
    # 6 очередей, 2 эксченджа, из 6 - 2 dlq, 2 очереди для постинга запросов на отправку,
    # 2 очереди для сохранения посланных сообщений в бд
    connection = await aio_pika.connect_robust(settings.rabbitmq_connection_url)
    async with connection:
        channel = await connection.channel()

        await channel.declare_exchange(settings.default_exchange, aio_pika.ExchangeType.DIRECT)
        await channel.declare_exchange(settings.dlx_exchange, aio_pika.ExchangeType.DIRECT)

        instant_message_dlq = await channel.declare_queue(settings.instant_message_dlq, durable=True)
        instant_notification_dlq = await channel.declare_queue(settings.instant_notification_dlq, durable=True)

        await channel.declare_queue(
            settings.instant_message_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.instant_message_dlq
            }
        )

        await channel.declare_queue(
            settings.scheduled_message_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.instant_message_dlq
            }
        )

        await channel.declare_queue(
            settings.instant_notification_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.instant_notification_dlq
            }
        )

        await channel.declare_queue(
            settings.scheduled_notification_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.dlx_exchange,
                'x-dead-letter-routing-key': settings.instant_notification_dlq,

            }
        )

        await instant_message_dlq.bind(exchange=settings.dlx_exchange, routing_key=settings.instant_message_dlq)
        await instant_notification_dlq.bind(exchange=settings.dlx_exchange,
                                            routing_key=settings.instant_notification_dlq)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(initialize_rabbitmq())

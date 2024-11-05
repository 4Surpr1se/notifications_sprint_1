import asyncio
import logging

from consumer_messages.consumers.instant_consumer import InstantConsumer

# from consumers.scheduled_consumer import ScheduledConsumer

logging.basicConfig(level=logging.INFO)


async def main():
    consumers = [InstantConsumer(),
                 # ScheduledConsumer(),
                 ]

    for consumer in consumers:
        await consumer.start()

if __name__ == "__main__":
    asyncio.run(main())
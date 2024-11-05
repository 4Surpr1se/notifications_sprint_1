import json
from fastapi import HTTPException
import aio_pika
from notification_gen_app.schemas.messages import InstantMessageRequest, WelcomeLinkMessageRequest

class MessageService:
    def __init__(self, channel, delivery_mode=2):
        self.channel = channel
        self.delivery_mode = delivery_mode

    async def send_single_message(self, content_id, message: InstantMessageRequest, message_transfer, queue_name):
        try:
            # Prepare the message body to be sent to RabbitMQ
            message_body = json.dumps({
                "content_id": str(content_id),
                "email": message.email,
                "message_transfer": message_transfer,
                "message_type": "instant",
                "message_data": message.message_data
            })

            # Publish the message to the queue
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message_body.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT if self.delivery_mode == 2 else aio_pika.DeliveryMode.NON_PERSISTENT
                ),
                routing_key=queue_name
            )

            return {"status": "Message sent to broker", "data": message_body}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message to broker: {str(e)}")

    async def send_welcome_message(self, user_email, message: dict, message_transfer, queue_name):
        try:
            # Prepare the message body to be sent to RabbitMQ
            message_body = json.dumps({
                "email": user_email,
                "message_transfer": message_transfer,
                "message_type": "welcome",
                "message_data": message,
            })

            # Publish the message to the queue
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message_body.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT if self.delivery_mode == 2 else aio_pika.DeliveryMode.NON_PERSISTENT
                ),
                routing_key=queue_name
            )

            return {"status": "Message sent to broker", "data": message_body}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message to broker: {str(e)}")
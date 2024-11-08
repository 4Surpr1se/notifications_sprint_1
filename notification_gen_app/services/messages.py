import json

from functools import lru_cache

from fastapi import Depends
from notification_gen_app.schemas.messages import InstantMessageRequest
from notification_gen_app.services.broker_service import RabbitMQService


class MessageSendException(Exception):
    pass


class MessageService:
    def __init__(self, broker_service: RabbitMQService = Depends()):
        self.broker_service = broker_service

    async def send_single_message(self, content_id, message: InstantMessageRequest, message_transfer, queue_name):
        try:
            message_body = json.dumps({
                "content_id": str(content_id),
                "email": message.email,
                "message_transfer": message_transfer,
                "message_type": "instant",
                "message_data": message.message_data
            })
            return await self.broker_service.publish(message_body, queue_name)

        except Exception as e:
            raise MessageSendException("Failed to send message to broker: %s" % str(e))

    async def send_welcome_message(self, user_email, message: dict, message_transfer, queue_name):
        try:
            message_body = json.dumps({
                "email": user_email,
                "message_transfer": message_transfer,
                "message_type": "welcome",
                "message_data": message,
            })
            return await self.broker_service.publish(message_body, queue_name)

        except Exception as e:
            raise MessageSendException("Failed to send message to broker: %s" % str(e))


@lru_cache
def get_message_service(message_service: MessageService = Depends()):
    return message_service

import jwt
import aio_pika
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from notification_gen_app.config import scheduler_settings
from notification_gen_app.config.settings import settings
from notification_gen_app.services.messages import MessageService
from notification_gen_app.services.periodic_messages import PeriodicTaskService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_rabbitmq_channel():
    # Set up an asynchronous connection to RabbitMQ
    connection = await aio_pika.connect_robust(settings.rabbitmq_connection_url)
    channel = await connection.channel()
    try:
        yield channel
    finally:
        await channel.close()
        await connection.close()


async def get_message_service(rabbitmq_channel=Depends(get_rabbitmq_channel)):
    message_service = MessageService(channel=rabbitmq_channel)

    try:
        yield message_service
    finally:
        # Ensure the channel and connection are closed in the cleanup of get_rabbitmq_channel
        pass  # Cleanup is handled by get_rabbitmq_channel

async def get_periodic_task_service():
    task_service = PeriodicTaskService(scheduler=scheduler_settings.scheduler)
    try:
        yield task_service
    finally:
        pass

def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])

        # Extract user information
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        # Return the extracted user information
        return {"user_id": user_id, "email": email}

    except PyJWTError:
        raise HTTPException(status_code=403, detail="Could not validate token")
import os
from datetime import timedelta
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project settings
    base_dir: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = "consumer_app"

    # RabbitMQ connection settings
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_connection_port: int = 5672
    rabbitmq_management_port: int = 15672
    rabbitmq_default_user: str = "guest"
    rabbitmq_default_pass: str = "guest"

    # RabbitMQ queue and exchange settings
    dlx_exchange: str = "dlx_exchange"
    instant_dlq: str = "instant_dlq"
    scheduled_dlq: str = "scheduled_dlq"
    instant_message_queue: str = "instant_message"
    scheduled_message_queue: str = "scheduled_message"
    instant_notification_queue: str = "instant_notification"
    scheduled_notification_queue: str = "scheduled_notification"

    # Middleware settings
    middleware_secret_key: str

    # JWT settings
    secret_key: str

    # Short link settings
    redirect_url: str = "http://localhost:8000/"
    expires_in: timedelta = timedelta(hours=48)
    confirmation_base_url: str = "http://localhost:8000/confirm-email"

    # Redis
    redis_host: str = "redis"
    redis_port: int = "6379"

    @property
    def rabbitmq_connection_url(self) -> str:
        return f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@{self.rabbitmq_host}:{self.rabbitmq_connection_port}/"


settings = Settings()
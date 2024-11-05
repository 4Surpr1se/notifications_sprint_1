import os
from datetime import timedelta
from typing import ClassVar
from pika import ConnectionParameters, PlainCredentials
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
    instant_notification_queue: str = "instant_notification"
    scheduled_message_queue: str = "scheduled_message"
    scheduled_notification_queue: str = "scheduled_notification"

    # SMTP settings
    smtp_pass: str = 'SMTP_PASS'
    smtp_email: str = 'SMTP_EMAIL'
    smtp_host: str = 'smtp.yandex.ru'
    smtp_port: int = 465

    # PostgreSQL settings
    postgres_host: str = 'postgres'
    postgres_user: str = 'practix_user'
    postgres_password: str = 'practix_password'
    postgres_db: str = 'notification_db'
    postgres_port: int = 5432

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def rabbitmq_connection_url(self) -> str:
        return f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@{self.rabbitmq_host}:{self.rabbitmq_connection_port}/"


settings = Settings()
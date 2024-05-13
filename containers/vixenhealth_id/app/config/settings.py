import logging
from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    DRIVER: str = "postgresql+"
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432
    POSTGRES_NAME: str

    MINIO_HOST: str = Field(alias="MINIO_ROOT_HOST")
    MINIO_USER: str = Field(alias="MINIO_ROOT_USER")
    MINIO_PASSWORD: str = Field(alias="MINIO_ROOT_PASSWORD")

    RABBIT_HOST: str = Field(alias="RABBITMQ_DEFAULT_HOST")
    RABBIT_USER: str = Field(alias="RABBITMQ_DEFAULT_USER")
    RABBIT_PASS: str = Field(alias="RABBITMQ_DEFAULT_PASS")

    PROJECT_SECRET_KEY: str

    DEBUG: bool = True
    LOG_LEVEL: int = logging.INFO

    PROJECT_VERSION: str

    @cached_property
    def database_url(self) -> URL:
        database_url = URL(
            drivername=self.DRIVER + "asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_NAME,
            query={}  # type: ignore
        )
        return database_url


settings = Settings()  # type: ignore

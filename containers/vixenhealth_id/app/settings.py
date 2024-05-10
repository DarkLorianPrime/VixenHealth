from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str

    MINIO_HOST: str = Field(alias="MINIO_ROOT_HOST")
    MINIO_USER: str = Field(alias="MINIO_ROOT_USER")
    MINIO_PASSWORD: str = Field(alias="MINIO_ROOT_PASSWORD")

    RABBIT_HOST: str = Field(alias="RABBITMQ_DEFAULT_HOST")
    RABBIT_USER: str = Field(alias="RABBITMQ_DEFAULT_USER")
    RABBIT_PASSWORD: str = Field(alias="RABBITMQ_DEFAULT_PASSWORD")

    PROJECT_SECRET_KEY: str


settings = Settings()  # type: ignore

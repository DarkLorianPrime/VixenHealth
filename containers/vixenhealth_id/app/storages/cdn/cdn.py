from minio import Minio

from config.settings import settings


def get_minio():
    return Minio(
        f"{settings.MINIO_HOST}:9000",
        access_key=settings.MINIO_USER,
        secret_key=settings.MINIO_PASSWORD
    )

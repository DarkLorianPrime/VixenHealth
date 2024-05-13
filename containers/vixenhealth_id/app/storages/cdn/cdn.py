from minio import Minio

from config.settings import settings

AVATAR_BUCKET_NAME = "avatars"


def get_minio():
    return Minio(
        f"{settings.MINIO_HOST}:9000",
        access_key=settings.MINIO_USER,
        secret_key=settings.MINIO_PASSWORD
    )


def init_minio():
    minio = get_minio()
    if not minio.bucket_exists(AVATAR_BUCKET_NAME):
        minio.make_bucket(AVATAR_BUCKET_NAME)

        with open("assets/default.png", "rb") as default_avatar:
            minio.put_object(
                bucket_name=AVATAR_BUCKET_NAME,
                object_name="default.png",
                data=default_avatar,
                length=-1,
                part_size=10485760
            )

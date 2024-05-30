from minio import Minio

from config.settings import settings

AVATAR_BUCKET_NAME = "avatars"


def get_minio():
    return Minio(
        f"{settings.MINIO_HOST}:9000",
        access_key=settings.MINIO_USER,
        secret_key=settings.MINIO_PASSWORD,
        secure=False,
    )


def exists_or_create(minio: Minio, bucket_name: str):
    bucket_exists = minio.bucket_exists(bucket_name)
    if not bucket_exists:
        minio.make_bucket(bucket_name)

    return bucket_exists


def init_minio():
    minio = get_minio()
    if not exists_or_create(minio, AVATAR_BUCKET_NAME):
        with open("storages/cdn/assets/default.png", "rb") as default_avatar:
            minio.put_object(
                bucket_name=AVATAR_BUCKET_NAME,
                object_name="default.png",
                data=default_avatar,
                length=-1,
                part_size=10485760,
            )

import abc
import datetime
import uuid
from abc import abstractmethod
from typing import Annotated

from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_mixin, mapped_column, Mapped, DeclarativeBase
from sqlalchemy import DateTime, func, UUID, Boolean

from storages.cdn.cdn import get_minio
from storages.database.database import get_session


@declarative_mixin
class CreatedUpdatedMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, onupdate=func.now(), server_default=func.now()
    )


@declarative_mixin
class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    at_deleted: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True, default=None
    )


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, primary_key=True
    )


class BaseRepository(abc.ABC):
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        minio: Annotated[Minio, Depends(get_minio)],
    ):
        self.session = session
        self.minio = minio

    @abstractmethod
    async def is_exists(self, *args, **kwargs):
        """exists"""
        raise NotImplementedError

    @abstractmethod
    async def find(self, *args, **kwargs):
        """limit 1"""
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

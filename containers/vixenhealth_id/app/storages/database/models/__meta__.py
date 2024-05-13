import datetime
import uuid

from sqlalchemy.orm import declarative_mixin, mapped_column, Mapped, DeclarativeBase
from sqlalchemy import DateTime, func, UUID, Boolean


@declarative_mixin
class CreatedUpdatedMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,
                                                          server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime,
                                                          onupdate=func.now(),
                                                          server_default=func.now())


@declarative_mixin
class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    at_deleted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True, default=None)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        primary_key=True
    )

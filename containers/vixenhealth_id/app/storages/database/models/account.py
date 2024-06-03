import uuid
from enum import Enum
from typing import List

from sqlalchemy import (
    String,
    UUID,
    ForeignKey,
    Index,
    Boolean,
    Enum as SqlEnum,
    DateTime,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin
from storages.database.types.file import File
from storages.database.models.passport import Passport
from storages.database.models.role import Role, account_roles
from storages.database.models.permission import Permission, account_permissions

oauth_account = Table(
    "oauth_account",
    Base.metadata,
    Column("account_id", UUID(as_uuid=True), ForeignKey("account.id")),
    Column("oauth_service_id", UUID(as_uuid=True), ForeignKey("oauth_service.id")),
    Column("service_account_id", String, nullable=False),
    Column("connected_at", DateTime()),
)


class OauthServiceType(Enum):
    yandex = "Yandex"
    vk = "VK"


class OauthService(Base):
    __tablename__ = "oauth_service"

    type: Mapped[str] = mapped_column(SqlEnum(OauthServiceType), nullable=False)

    __table_args__ = (Index("oauth_type", "type", unique=True),)


class Account(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(
        File(bucket_name="avatars"), nullable=False, default="default.png"
    )
    need_change_password: Mapped[bool] = mapped_column(Boolean, default=False)
    passport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passport.id"), default=None, nullable=True
    )

    passport: Mapped["Passport"] = Relationship(lazy="selectin")
    roles: Mapped[List["Role"]] = Relationship(secondary=account_roles, lazy="selectin")
    permissions: Mapped[List["Permission"]] = Relationship(
        secondary=account_permissions, lazy="selectin"
    )
    account_oauth: Mapped[List["OauthService"]] = Relationship(
        secondary=oauth_account, lazy="selectin"
    )
    __table_args__ = (
        Index(
            "account_username_email_password",
            "username",
            "email",
            "password",
            unique=True,
        ),
    )

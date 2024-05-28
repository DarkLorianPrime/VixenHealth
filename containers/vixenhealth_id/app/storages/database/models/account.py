import uuid
from typing import List

from sqlalchemy import String, UUID, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin
from storages.database.types.file import File
from storages.database.models.passport import Passport
from storages.database.models.role import Role, account_roles
from storages.database.models.permission import Permission, account_permissions


class Account(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(
        File(bucket_name="avatars"), nullable=False, default="default.png"
    )
    need_change_password: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=None
    )
    passport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passport.id"), default=None, nullable=True
    )
    passport: Mapped["Passport"] = Relationship(lazy="selectin")
    roles: Mapped[List["Role"]] = Relationship(secondary=account_roles, lazy="selectin")
    permissions: Mapped[List["Permission"]] = Relationship(
        secondary=account_permissions, lazy="selectin"
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

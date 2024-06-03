from typing import List

from sqlalchemy import String, Table, Column, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models import Base
from storages.database.models.permission import Permission

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("role.id")),
    Column("permission_id", ForeignKey("permission.id")),
    Column("application_id", ForeignKey("application.id")),
)

account_roles = Table(
    "account_roles",
    Base.metadata,
    Column("role_id", ForeignKey("role.id")),
    Column("account_id", ForeignKey("account.id")),
    Column("application_id", ForeignKey("application.id")),
)


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String)
    permissions: Mapped[List["Permission"]] = Relationship(
        secondary=role_permissions, lazy="selectin"
    )

    __table_args__ = (Index("role_name", "name", unique=True),)

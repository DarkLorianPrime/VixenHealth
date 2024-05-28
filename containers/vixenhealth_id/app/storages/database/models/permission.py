from sqlalchemy import String, Table, Column, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from storages.database.models import Base

account_permissions = Table(
    "account_permissions",
    Base.metadata,
    Column("account_id", ForeignKey("account.id")),
    Column("permission_id", ForeignKey("permission.id")),
    Column("application_id", ForeignKey("application.id")),
)


class Permission(Base):
    __tablename__ = "permission"

    name: Mapped[str] = mapped_column(String)
    codename: Mapped[str] = mapped_column(String)

    __table_args__ = (
        Index("permission_name_codename", "name", "codename", unique=True),
    )

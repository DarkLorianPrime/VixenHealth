from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin
from storages.database.types.file import File


class Account(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(File, nullable=False, default="avatars/default.png")

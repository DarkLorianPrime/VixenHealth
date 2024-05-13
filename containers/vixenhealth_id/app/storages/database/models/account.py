import datetime
import uuid

from sqlalchemy import String, Boolean, Integer, Date, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin
from storages.database.types.file import File


class Passport(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "passport"

    first_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String)
    sex: Mapped[bool] = mapped_column(Boolean)  # давай
    series: Mapped[int] = mapped_column(Integer)
    number: Mapped[int] = mapped_column(Integer)
    subdiv_code: Mapped[str] = mapped_column(String)
    issue_date: Mapped[datetime.date] = mapped_column(Date)
    issuing_place: Mapped[str] = mapped_column(String)
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    birth_place: Mapped[str] = mapped_column(String)


class Account(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(File(bucket_name="avatars"), nullable=False, default="default.png")
    passport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("passport.id"),
        default=None,
        nullable=True
    )
    passport: Mapped["Passport"] = Relationship()

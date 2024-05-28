import datetime

from sqlalchemy import String, Boolean, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin


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

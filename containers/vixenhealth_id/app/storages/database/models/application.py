from sqlalchemy import String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column

from storages.database.models import Base


class Application(Base):
    """default structure (literally template)"""

    __tablename__ = "application"

    name: Mapped[str] = mapped_column(String)
    subdomain: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    public: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("application_description_name", "description", "name", unique=True),
        Index("application_name", "name", unique=True),
    )

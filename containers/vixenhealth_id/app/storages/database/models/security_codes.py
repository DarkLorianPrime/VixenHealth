import uuid
import datetime

from sqlalchemy import (
    func,
    DateTime,
    String,
    UUID,
    ForeignKey,
    Interval,
    Enum as SqlEnum,
)
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models import Base, Account


class CodeType(Enum):
    TwoFactor = "2fa"
    OnRegistration = "continue_registration"
    ResetPassword = "reset_password"
    SuspendActivity = "suspend_activity"
    ChangeData = "change_data"


class SecurityCodes(Base):
    __tablename__ = "security_code"

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    code: Mapped[str] = mapped_column(String)
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("account.id"), nullable=False
    )
    lifetime: Mapped[datetime.timedelta] = mapped_column(
        Interval, default=datetime.timedelta(days=1)
    )
    type: Mapped[str] = mapped_column(SqlEnum(CodeType), nullable=False)
    change_uri: Mapped[str] = mapped_column(String, nullable=True)  # maybe not needed

    account: Mapped["Account"] = Relationship(lazy="selectin")

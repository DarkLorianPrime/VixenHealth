import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from storages.database.models.__meta__ import Base, SoftDeleteMixin, CreatedUpdatedMixin
from storages.database.types.bytestring import ByteString
from storages.database.types.file import File
from storages.database.models.passport.passport import Passport


class Account(Base, SoftDeleteMixin, CreatedUpdatedMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(File(bucket_name="avatars"), nullable=False, default="default.png")
    access_mask: Mapped[bytes] = mapped_column(ByteString)
    passport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("passport.id"),
        default=None,
        nullable=True
    )
    passport: Mapped["Passport"] = Relationship()




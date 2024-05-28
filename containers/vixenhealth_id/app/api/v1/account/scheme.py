import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class PassportResponseScheme(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    sex: bool
    birth_date: datetime.date
    birth_place: str


class ProfileResponseScheme(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    avatar: str
    created_at: datetime.datetime
    passport: Optional[PassportResponseScheme]

import datetime
import uuid
from typing import Literal, Dict

from pydantic import BaseModel, field_validator

from api.v1.authentication.validators import (
    email_validate,
    password_validate,
    username_validate,
)
from utils.schema import CustomModel


class CreateAccountReturningSchema(BaseModel):
    id: uuid.UUID | None
    created_at: datetime.datetime | None


class CreateAccountReturnSchema(BaseModel):
    data: CreateAccountReturningSchema | Dict = {}
    status: Literal["success", "failure"] = "success"

    class Meta:
        orm_mode = True


class CreateAccountRequestSchema(CustomModel):
    username: str
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_validator(cls, value: str) -> str:
        return email_validate(value)

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return password_validate(value)

    @field_validator("username")
    @classmethod
    def username_validator(cls, value: str) -> str:
        return username_validate(value)


class AuthenticateAccountRequestSchema(CustomModel):
    login: str
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return password_validate(value)


class TokensResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshAccountRequestSchema(CustomModel):
    refresh_token: str


class OauthRequestSchema(CustomModel):
    token: str

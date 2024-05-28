import re

from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from api.v1.authentication.responses import Exceptions


def username_validate(value: str) -> str:
    if not re.fullmatch(r"^[A-Za-z0-9]{4,32}$", value):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Exceptions.USERNAME_NOT_VALID,
        )

    return value


def password_validate(password: str) -> str:
    if not re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Exceptions.NOT_VALID_CYRILLIC_OR_LENGTH,
        )

    return password


def email_validate(value: str) -> str:
    if not re.fullmatch(r"^\S+@\S+\.\S+$", value):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=Exceptions.EMAIL_NOT_VALID
        )

    return value

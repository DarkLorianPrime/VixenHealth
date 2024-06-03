from datetime import timedelta, datetime
from typing import Any, Dict

import jwt
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from config.settings import settings
from api.v1.authentication.responses import Exceptions


async def create_token(expires: datetime, payload_data: Dict[str, Any]) -> str:
    payload = {"exp": expires, **payload_data}

    ready_jwt = jwt.encode(
        payload=payload, algorithm=settings.JWT_ALGORITHM, key=settings.JWT_SECRET_KEY
    )
    return ready_jwt


async def create_access_token(payload_data: Dict[str, Any]) -> str:
    expires = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRE)
    return await create_token(expires, payload_data)


async def create_refresh_token(payload_data: Dict[str, Any]) -> str:
    expires = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRE)
    return await create_token(expires, payload_data)


async def get_credentials_from_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, algorithms=[settings.JWT_ALGORITHM], key=settings.JWT_SECRET_KEY
        )
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=Exceptions.INVALID_TOKEN_ACCESS
        )

    return payload

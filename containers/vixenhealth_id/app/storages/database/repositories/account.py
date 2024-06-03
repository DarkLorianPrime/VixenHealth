import datetime
from typing import Annotated, Optional, Dict, Any, Union, Literal, List, Iterable

from fastapi import Depends, HTTPException
from minio import Minio
from sqlalchemy import insert, select, or_, and_, exists, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from starlette.requests import Request
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)

from config.settings import settings
from api.v1.authentication.responses import Exceptions
from storages.cdn.cdn import get_minio
from storages.database.database import get_session
from storages.database.models import Account, Role, Permission
from storages.database.models.__meta__ import BaseRepository
from argon2 import PasswordHasher

from storages.database.models.account import (
    OauthService,
    oauth_account,
    OauthServiceType,
)
from utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    get_credentials_from_token,
)

hasher = PasswordHasher()


class AccountRepository(BaseRepository):
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        minio: Annotated[Minio, Depends(get_minio)],
    ):
        super().__init__(session, minio)
        self.model = Account

    async def create(
        self, credentials: Dict[str, Any], *returning: InstrumentedAttribute
    ) -> Dict[str, Union[str, Row, Dict[str, Any]]]:
        stmt = insert(self.model).values(**credentials).returning(*returning)
        result = await self.session.execute(stmt)

        returning_fields = result.first()

        if returning_fields:
            await self.session.commit()
            return {"data": returning_fields}

        return {"status": "failure"}

    async def find(self, account_id: str):
        stmt = (
            select(self.model)
            .where(self.model.id == account_id, self.model.is_deleted.is_(False))
            .limit(1)
        )

        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_by_credentials(
        self, hashed_password: str, login: str
    ) -> Optional["Account"]:
        stmt = select(self.model).where(
            and_(
                or_(self.model.email == login, self.model.username == login),
                self.model.password == hashed_password,
                self.model.is_deleted.is_(False),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar()

    async def authenticate(self, credentials: Dict[str, Any]):
        credentials["hashed_password"] = await self.hash_password(
            credentials.pop("password", "")
        )
        account = await self.get_by_credentials(**credentials)
        if not account:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=Exceptions.LOGIN_OR_PASSWORD_NF
            )
        return await self.generate_tokens(account)

    async def parse_payload_model(self, models: Iterable[Role | Permission]):
        new_data = []
        for model in models:
            new_data.append({"id": str(model.id)})

        return new_data

    async def generate_tokens(self, account: Account):
        payload = {
            "sub": str(account.id),
            "permissions": await self.parse_payload_model(account.permissions),
            "roles": await self.parse_payload_model(account.roles),
        }
        return {
            "access_token": await create_access_token(payload),
            "refresh_token": await create_refresh_token(payload),
        }

    async def hash_password(self, password: str) -> str:
        return hasher.hash(password, salt=settings.PROJECT_SECRET_KEY.encode())

    async def create_user(self, credentials, *returning):
        credentials["password"] = await self.hash_password(credentials["password"])
        return await self.create(credentials, *returning)

    async def is_exists(self, is_or_: bool = False, *args):
        args = args if not is_or_ else (or_(*args),)
        stmt = exists(self.model).where(*args).select()
        result = await self.session.execute(stmt)

        return result.scalar()

    async def update_refresh_token(self, refresh_token: str):
        payload: Dict[str, Any] = await get_credentials_from_token(refresh_token)
        expired_time = datetime.datetime.fromtimestamp(payload["exp"])

        if expired_time > datetime.datetime.now():
            # todo: release delete from database
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=Exceptions.REFRESH_TOKEN_EXPIRED,
            )

        account = await self.find(payload["sub"])
        if account is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=Exceptions.INVALID_TOKEN_REFRESH
            )

        return {
            "access_token": await create_access_token(payload),
            "refresh_token": await create_refresh_token(payload),
        }


async def get_account(
    request: Request, repository: Annotated[AccountRepository, Depends()]
) -> Account | None:
    payload: Dict[str, str] = request.state.jwt_payload
    if payload is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Need call JWTBearer first"
        )

    account_id: str | None = payload.get("sub")
    if account_id is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="'Sub' is not defined"
        )

    account = await repository.find(account_id)
    if not account:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if account.need_change_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Your password is the default. Please, setup your account.",
        )

    return account

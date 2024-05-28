from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.authentication.scheme import (
    CreateAccountRequestSchema,
    AuthenticateAccountRequestSchema,
)
from storages.database.database import get_session
from storages.database.models import Account
from storages.database.repositories.account import AccountRepository


class Service:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        repository: Annotated[AccountRepository, Depends()],
    ):
        self.session = session
        self.repository = repository

    async def is_user_exists(self, credentials: CreateAccountRequestSchema):
        return await self.repository.is_exists(
            True,
            Account.username == credentials.username,
            Account.email == credentials.email,
        )

    async def create_account(self, credentials: CreateAccountRequestSchema) -> Account:
        return await self.repository.create_user(
            credentials.dict(), Account.id, Account.created_at
        )

    async def authenticate_user(self, credentials: AuthenticateAccountRequestSchema):
        return await self.repository.authenticate(credentials.dict())

    async def update_refresh(self, refresh_token: str):
        return await self.repository.update_refresh_token(refresh_token)

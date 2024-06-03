from typing import Annotated, Dict, Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from api.v1.authentication.responses import Exceptions
from api.v1.authentication.scheme import (
    CreateAccountRequestSchema,
    AuthenticateAccountRequestSchema,
)
from config.settings import async_client, settings
from storages.database.database import get_session
from storages.database.models import Account
from storages.database.models.account import OauthServiceType
from storages.database.repositories.account import AccountRepository

VK_OAUTH_URL = "https://oauth.vk.com/access_token"
YANDEX_OAUTH_URL = "https://login.yandex.ru/info"


class OauthService:
    def __init__(self, session: AsyncSession, repository: AccountRepository):
        self.session = session
        self.repository = repository

    async def get_by_credentials(
        self, service: OauthServiceType, status_code: int, credentials: Dict[str, Any]
    ):
        if status_code != 200:
            raise HTTPException(
                status_code=status_code, detail=Exceptions.TOKEN_NOT_AVAILABLE
            )

        if credentials.get("expires_in", 10001) < 10000:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail=Exceptions.TOKEN_IS_EXPIRED
            )

        account = await self.repository.get_by_oauth(
            service,
            credentials.get("user_id" if service == OauthServiceType.vk else "psuid"),
        )

        if account is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=Exceptions.ACCOUNT_NOT_RELATED
            )

        return await self.repository.generate_tokens(account)

    async def get_by_ya_credentials(self, token: str) -> Dict[str, str]:
        result = await async_client.get(
            YANDEX_OAUTH_URL, headers={"Authorization": f"Bearer {token}"}
        )
        account_tokens = await self.get_by_credentials(
            OauthServiceType.yandex, result.status_code, result.json()
        )
        return account_tokens

    async def get_by_vk_credentials(self, token: str) -> Dict[str, str]:
        result = await async_client.get(
            VK_OAUTH_URL,
            params={
                "client_id": settings.VK_OAUTH_CLIENT_ID,
                "client_secret": settings.VK_OAUTH_CLIENT_SECRET,
                "redirect_uri": settings.VK_OAUTH_ENDPOINT,
                "code": token,
            },
        )

        account_tokens = await self.get_by_credentials(
            OauthServiceType.vk, result.status_code, result.json()
        )

        return account_tokens


class Service:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        repository: Annotated[AccountRepository, Depends()],
    ):
        self.session = session
        self.repository = repository
        self.oauth = OauthService(session, repository)

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

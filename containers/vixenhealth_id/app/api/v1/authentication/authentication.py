from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.v1.authentication.responses import Exceptions
from api.v1.authentication.scheme import (
    CreateAccountRequestSchema,
    CreateAccountReturnSchema,
    AuthenticateAccountRequestSchema,
    TokensResponseSchema,
    RefreshAccountRequestSchema,
)
from api.v1.authentication.service import Service

token_router = APIRouter(prefix="/token", tags=["authentication", "token"])
oauth_router = APIRouter(prefix="/oauth", tags=["authentication", "oauth"])


@token_router.post(
    "/create/", status_code=HTTP_201_CREATED, response_model=CreateAccountReturnSchema
)
async def create_account(
    credentials: Annotated[
        CreateAccountRequestSchema, Depends(CreateAccountRequestSchema.as_form)
    ],
    service: Annotated[Service, Depends()],
):
    if await service.is_user_exists(credentials):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=Exceptions.ACCOUNT_EXISTS
        )

    return await service.create_account(credentials)


@token_router.post("/", response_model=TokensResponseSchema)
async def create_access_token(
    credentials: Annotated[
        AuthenticateAccountRequestSchema,
        Depends(AuthenticateAccountRequestSchema.as_form),
    ],
    service: Annotated[Service, Depends()],
):
    return await service.authenticate_user(credentials)


@token_router.post("/refresh", response_model=TokensResponseSchema)
async def refresh_access_token(
    credentials: Annotated[
        RefreshAccountRequestSchema, Depends(RefreshAccountRequestSchema.as_form)
    ],
    service: Annotated[Service, Depends()],
):
    return await service.update_refresh(credentials.refresh_token)


@oauth_router.post("/vk")
async def oauth_vk(): ...


@oauth_router.post("/yandex")
async def oauth_ya(): ...

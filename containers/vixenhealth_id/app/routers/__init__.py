from fastapi import APIRouter

from routers.account.account import account_router
from routers.authentication.authentication import token_router

profile_router = APIRouter(
    prefix='/profile',
    tags=["profile"]
)

settings_router = APIRouter(
    prefix='/settings',
    tags=["settings"]
)

account_router.include_router(token_router)
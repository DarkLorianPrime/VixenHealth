from fastapi import APIRouter

from api.v1.account.account import account_router
from api.v1.authentication.authentication import token_router, oauth_router

profile_router = APIRouter(prefix="/profile", tags=["profile"])

settings_router = APIRouter(prefix="/settings", tags=["settings"])

account_router.include_router(oauth_router)
account_router.include_router(token_router)

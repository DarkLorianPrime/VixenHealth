from typing import Annotated, Any

from fastapi import APIRouter, Depends

from api.v1.account.scheme import ProfileResponseScheme
from storages.database.repositories.account import get_account
from storages.database.models import Account
from utils.security_bearer import JWTBearer

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.get(
    "/me", dependencies=[Depends(JWTBearer())], response_model=ProfileResponseScheme
)
async def get_my_account(account: Annotated[Account, Depends(get_account)]) -> Any:
    return account

from fastapi import APIRouter

from api.v1 import settings_router
from api.v1 import account_router
from api.v1 import profile_router

v1_router = APIRouter(prefix="/v1", tags=["api_v1_version"])

v1_router.include_router(profile_router)
v1_router.include_router(account_router)
v1_router.include_router(settings_router)

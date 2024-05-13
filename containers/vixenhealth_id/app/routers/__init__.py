from fastapi import APIRouter


authentication_router = APIRouter(
    prefix='/auth',
    tags=["authentication"]
)

profile_router = APIRouter(
    prefix='/profile',
    tags=["profile"]
)

settings_router = APIRouter(
    prefix='/settings',
    tags=["settings"]
)
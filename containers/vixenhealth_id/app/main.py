from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from routers import authentication_router, settings_router, profile_router
from prometheus_fastapi_instrumentator import Instrumentator

from storages.cdn.cdn import init_minio


def connect_routers(application: FastAPI) -> None:
    main_api_router = APIRouter(prefix="/api/v1")
    main_api_router.include_router(authentication_router)
    main_api_router.include_router(settings_router)
    main_api_router.include_router(profile_router)
    application.include_router(main_api_router)


def connect_utils(application: FastAPI) -> None:
    Instrumentator(
        excluded_handlers=["/metrics"]
    ).instrument(application).expose(application)


@asynccontextmanager
async def lifespan_starlette(_):
    init_minio()
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="VixenHealth ID",
        description="Сервис, отвечающий за аутентификацию и взаимодействие с профилем пользователей.",
        version="0.0.3",
        lifespan=lifespan_starlette
    )
    connect_routers(application)
    connect_utils(application)
    return application


app = create_app()

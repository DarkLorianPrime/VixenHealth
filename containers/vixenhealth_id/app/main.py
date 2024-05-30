from fastapi import FastAPI, APIRouter
from pydantic import ValidationError

from api import v1_router
from config.settings import settings
from prometheus_fastapi_instrumentator import Instrumentator

from utils.exceptions import pydantic_exception_handler
from utils.lifespan import lifespan


def connect_routers(application: FastAPI) -> None:
    main_api_router = APIRouter(prefix="/api")

    main_api_router.include_router(v1_router)
    application.include_router(main_api_router)


def connect_utils(application: FastAPI) -> None:
    Instrumentator(excluded_handlers=["/metrics"]).instrument(application).expose(
        application
    )
    application.add_exception_handler(ValidationError, pydantic_exception_handler)  # type: ignore


def create_app() -> FastAPI:
    application = FastAPI(
        title="VixenHealth ID",
        description="Сервис, отвечающий за аутентификацию и взаимодействие с профилем пользователей.",
        version=settings.PROJECT_VERSION,
        lifespan=lifespan,
    )
    connect_routers(application)
    connect_utils(application)
    return application


app = create_app()

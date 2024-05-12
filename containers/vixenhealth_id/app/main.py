from fastapi import FastAPI, APIRouter


def connect_routers(application: FastAPI) -> None:
    main_api_router = APIRouter(prefix="/api/v1")
    application.include_router(main_api_router)


def create_app() -> FastAPI:
    application = FastAPI(
        title="VixenHealth ID",
        description="Сервис, отвечающий за аутентификацию и взаимодействие с профилем пользователей.",
        version="0.0.1"
    )
    return application


app = create_app()

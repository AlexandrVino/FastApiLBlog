import contextlib
import os.path

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from .background_tasks import BackgroundTaskRunner
from .config import STATIC_PATH, Config
from .exceptions import get_exception_handlers
from .router import v1_router


def create_app(container: AsyncContainer, config: Config) -> FastAPI:
    """
    Фабрика для создания основного FastAPI-приложения.

    Настраивает жизненный цикл приложения (lifespan), CORS, обработчики ошибок,
    статические файлы и маршруты API. Также интегрирует DI-контейнер.
    """

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        """
        Контекстный менеджер для управления жизненным циклом приложения.

        Запускает фоновые задачи,
        а также корректно завершает работу при остановке.
        """

        runner = BackgroundTaskRunner(container)
        try:
            await runner.run_background_tasks()
            yield
        finally:
            await runner.cancel_background_task()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for exc_type, handler in get_exception_handlers():
        app.add_exception_handler(exc_type, handler)

    if not os.path.exists("static"):
        os.makedirs("static")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(v1_router, prefix="/api")

    @app.get("/")
    async def root():
        with open(STATIC_PATH / "index.html", encoding="utf8") as file:
            return HTMLResponse(file.read().format(FRONTEND_PATH=STATIC_PATH))

    setup_dishka(container, app)

    return app

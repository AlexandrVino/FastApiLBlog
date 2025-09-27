import asyncio
from datetime import timedelta
from typing import Any, Callable, Coroutine

from dishka import AsyncContainer


def background_task_runner(
    delay: timedelta,
) -> Callable[
    [Callable[..., Coroutine[Any, Any, Any]]],
    Callable[[AsyncContainer], Coroutine[Any, Any, None]],
]:
    """Декоратор для создания фоновых задач с заданным интервалом выполнения."""

    def _runner(func: Callable[..., Coroutine[..., ..., ...]]):
        async def _wrapper(container: AsyncContainer):
            while True:
                _ = await func(container)
                await asyncio.sleep(delay.total_seconds())

        return _wrapper

    return _runner


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BackgroundTaskRunner(metaclass=Singleton):
    def __init__(self, container: AsyncContainer):
        self.tasks: list[asyncio.Task] = []
        self.container = container

    async def run_background_tasks(self) -> list[asyncio.Task]:
        """
        Запускает все фоновые задачи приложения.

        Возвращает список созданных задач для последующего управления их жизненным циклом.
        """

        return self.tasks

    async def cancel_background_task(self):
        """
        Корректно останавливает все фоновые задачи.

        Последовательно отменяет каждую задачу и обрабатывает возможные ошибки отмены.
        """

        for task in self.tasks:
            try:
                task.cancel()
                await task
            except asyncio.CancelledError:
                continue


__all__ = [
    "BackgroundTaskRunner",
]

from functools import lru_cache
from pathlib import Path

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_PATH = Path(__file__).parent.parent.resolve()
STATIC_PATH = BACKEND_PATH / "static"


class Config(BaseSettings):
    """
    Конфигурация приложения, включающая настройки для различных сервисов и компонентов системы.

    Настройки загружаются из переменных окружения или файла `.env`. Класс предоставляет
    вычисляемые свойства для формирования URL-адресов подключения к внешним сервисам.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5000",
    ]

    server_host: str = "localhost"
    server_port: int = 5000

    admin_username: str
    admin_password: str
    base_url: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    secret_key: str

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_config() -> Config:
    return Config()

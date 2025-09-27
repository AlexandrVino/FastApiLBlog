from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Базовый класс моделей Pydantic с автоматическим преобразованием имён полей в camelCase."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ErrorModel(CamelModel):
    """Стандартная модель для возврата ошибок в API."""

    message: str

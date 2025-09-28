FROM python:3.11-slim

RUN pip3 install poetry

WORKDIR /app
COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install --no-root


COPY .. /app
CMD ./run_tests.sh
CMD ["poetry", "run", "uvicorn", "infrastructure.server:app", "--host", "0.0.0.0", "--port", "8080"]
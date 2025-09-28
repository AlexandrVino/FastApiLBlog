import asyncio
import os
import sys

import httpx
import pytest

from infrastructure.config import Config, get_config

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def config() -> Config:
    """Base URL of the running FastAPI Blog backend (can be Docker/uvicorn)."""
    return get_config()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL of the running FastAPI Blog backend (can be Docker/uvicorn)."""
    return "http://localhost:5000"


@pytest.fixture(scope="function")
async def client(base_url: str):
    from infrastructure.server import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport, base_url=base_url, timeout=httpx.Timeout(60)
    ) as c:
        yield c


@pytest.fixture(scope="function")
async def login(client):
    async def _wrapper(email, password="P@ssw0rd!"):
        response = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    return _wrapper


@pytest.fixture(scope="function")
async def admin_token(login, config) -> str | None:
    resp = await login(config.admin_username, config.admin_password)
    return resp["accessToken"]


@pytest.fixture(scope="function")
def unique_email():
    import random
    import time

    suffix = f"{int(time.time())}{random.randint(1000, 9999)}"
    name = "tester_" + suffix
    return f"{name}@example.com"

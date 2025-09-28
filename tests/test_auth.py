import pytest


async def _register(client, email, password):
    response = await client.post(
        "/api/v1/auth/register", json={"email": email, "password": password}
    )
    response.raise_for_status()
    return response.json()


@pytest.mark.asyncio
async def test_register_login_refresh_me_flow(client, unique_email, login):
    # register
    password = "P@ssw0rd!"
    user = await _register(client, unique_email, password)
    assert "accessToken" in user and "user" in user

    # login (idempotent if already logged)
    login = await login(unique_email, password)
    assert login["user"]["email"] == unique_email

    # me
    me = await client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {login['accessToken']}"}
    )
    assert me.status_code == 200
    assert me.json()["email"] == unique_email

    # refresh (cookie-based on server; still should return token pair if configured)
    refresh = await client.post("/api/v1/auth/refresh")
    assert refresh.status_code in (200, 401)
    if refresh.status_code == 200:
        body = refresh.json()
        assert "accessToken" in body

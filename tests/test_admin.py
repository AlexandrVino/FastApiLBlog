import os

import pytest


def require_admin(admin_token: str | None):
    print(admin_token)
    if not admin_token:
        pytest.skip("Set FASTAPI_ADMIN_TOKEN to run admin tests.")


@pytest.mark.asyncio
async def test_admin_users_crud_list_get_update(client, admin_token):
    require_admin(admin_token)
    # list users
    response = await client.get(
        "/api/v1/users/admin/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)

    if users:
        uid = users[0]["id"]
        response = await client.get(
            f"/api/v1/users/admin/{uid}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200

        # try updating role (no-op, set current role again)
        role = response.json().get("role", "USER")
        response_2 = await client.put(
            f"/api/v1/users/admin/{uid}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"role": role},
        )
        assert response_2.status_code in (200, 204)


@pytest.mark.asyncio
async def test_admin_categories_crud(client, admin_token):
    require_admin(admin_token)
    # create
    payload = {"title": "Тестовая категория", "description": "Интеграционный тест"}
    response = await client.post(
        "/api/v1/admin/categories/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload,
    )
    assert response.status_code in (200, 201)
    cat = response.json()
    cid = cat["id"]

    # list
    response = await client.get(
        "/api/v1/categories/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # get
    response = await client.get(
        f"/api/v1/categories/{cid}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200

    # update
    payload = {
        "id": cid,
        "title": "Тестовая категория (upd)",
        "description": "Обновлено",
    }
    response = await client.put(
        f"/api/v1/admin/categories/{cid}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload,
    )
    assert response.status_code in (200, 204)

    # delete
    response = await client.delete(
        f"/api/v1/admin/categories/{cid}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code in (200, 204, 202)


@pytest.mark.asyncio
async def test_admin_posts_crud(client, admin_token):
    require_admin(admin_token)
    # Ensure at least one category exists
    response = await client.get(
        "/api/v1/categories/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    cats = response.json()
    if not cats:
        response = await client.post(
            "/api/v1/admin/categories/",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Main", "description": ""},
        )
        assert response.status_code in (200, 201)
        cats = [response.json()]
    cid = cats[0]["id"]

    # create post
    payload = {
        "title": "Интеграционный пост",
        "body": "<p>Привет</p>",
        "category_id": cid,
    }
    response = await client.post(
        "/api/v1/admin/posts/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload,
    )
    assert response.status_code in (200, 201)

    post = response.json()
    pid = post["id"]

    # list admin
    response = await client.get(
        "/api/v1/posts/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # get admin
    response = await client.get(
        f"/api/v1/posts/{pid}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # update
    payload = {
        "id": pid,
        "title": "Интеграционный пост (upd)",
        "body": "<p>Обновлено</p>",
        "category_id": cid,
    }
    response = await client.put(
        f"/api/v1/admin/posts/{pid}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload,
    )
    assert response.status_code in (200, 204)

    # delete
    response = await client.delete(
        f"/api/v1/admin/posts/{pid}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in (200, 204, 202)

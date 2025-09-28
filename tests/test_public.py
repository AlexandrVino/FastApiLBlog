import pytest


@pytest.mark.asyncio
async def test_public_posts_and_categories(client):
    # lists should respond (may be empty)
    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200
    cats = response.json()
    assert isinstance(cats, list)

    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)

    # if there is at least one post, /posts/{id} should work
    if posts:
        pid = posts[0]["id"]
        response = await client.get(f"/api/v1/posts/{pid}")
        assert response.status_code == 200

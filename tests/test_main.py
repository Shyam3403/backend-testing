import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from main import app


transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_root():

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.get("/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_user():

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.get("/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Shyam"


@pytest.mark.asyncio
async def test_get_invalid_user():

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.get("/users/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user():

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post(
            "/users",
            json={
                "name": "Kumar"
            }
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Kumar"
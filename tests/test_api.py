# /Users/awaiskhan/work/personal/agentic-works/agentic-cto/projects/WebDataExtractor/tests/test_api.py

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_extract_data(client):
    response = await client.post("/api/extract", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "output" in data

@pytest.mark.asyncio
async def test_extract_data_failure(client):
    response = await client.post("/api/extract", json={"url": "https://nonexistentwebsite.com"})
    assert response.status_code == 200
    data = response.json()
    assert not data["success"]
    assert "error" in data

@pytest.mark.asyncio
async def test_organize_data(client):
    # Assuming there is an endpoint to organize data
    response = await client.post("/api/organize", json={"data": {"key": "value"}})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "output" in data

@pytest.mark.asyncio
async def test_organize_data_failure(client):
    # Assuming there is an endpoint to organize data
    response = await client.post("/api/organize", json={"data": {}})
    assert response.status_code == 200
    data = response.json()
    assert not data["success"]
    assert "error" in data
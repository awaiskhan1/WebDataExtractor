import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_extract_data():
    response = client.post("/api/extract", json={"url": "https://example.com", "extract_type": "text"})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_organize_data():
    response = client.post("/api/organize", json={"data": "test data", "format": "json"})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
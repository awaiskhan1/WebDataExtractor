import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRoutes:
    """Tests for API routes functionality."""
    
    def test_get_root_should_return_status_code_200(self):
        """Test that the root endpoint returns a 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_extract_endpoint(self):
        """Test the extract endpoint."""
        payload = {"url": "https://example.com", "extract_type": "text"}
        response = client.post("/api/extract", json=payload)
        assert response.status_code == 200
        assert "success" in response.json()

    def test_organize_endpoint(self):
        """Test the organize endpoint."""
        payload = {"data": "test data", "format": "json"}
        response = client.post("/api/organize", json=payload)
        assert response.status_code == 200
        assert "success" in response.json()
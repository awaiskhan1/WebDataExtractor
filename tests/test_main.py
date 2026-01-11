import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAppMain:
    """Tests for the main application functionality."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

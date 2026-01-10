import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

class TestRoutes:
    """Tests for API routes functionality."""
    
    def test_get_root_should_return_status_code_200(self):
        """Test that the root endpoint returns a 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to WebDataExtractor"}

    def test_get_task_list_should_return_status_code_200(self):
        """Test that the task list endpoint returns a 200 status code."""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_task_with_valid_data_should_return_status_code_201(self):
        """Test that creating a task with valid data returns a 201 status code."""
        payload = {
            "url": "https://example.com",
            "strategy": "scrape_links"
        }
        response = client.post("/tasks/", json=payload)
        assert response.status_code == 201
        assert isinstance(response.json(), dict)

    def test_create_task_with_invalid_data_should_return_status_code_400(self):
        """Test that creating a task with invalid data returns a 400 status code."""
        payload = {
            "url": "",
            "strategy": "scrape_links"
        }
        response = client.post("/tasks/", json=payload)
        assert response.status_code == 400
        assert isinstance(response.json(), dict)

    def test_get_task_details_with_valid_id_should_return_status_code_200(self):
        """Test that getting task details with a valid ID returns a 200 status code."""
        task_id = "123"
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_task_details_with_invalid_id_should_return_status_code_404(self):
        """Test that getting task details with an invalid ID returns a 404 status code."""
        task_id = "invalid_id"
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404
        assert isinstance(response.json(), dict)

    def test_delete_task_with_valid_id_should_return_status_code_204(self):
        """Test that deleting a task with a valid ID returns a 204 status code."""
        task_id = "123"
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

    def test_delete_task_with_invalid_id_should_return_status_code_404(self):
        """Test that deleting a task with an invalid ID returns a 404 status code."""
        task_id = "invalid_id"
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 404
        assert isinstance(response.json(), dict)
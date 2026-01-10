import pytest
from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from typing import Any

app = FastAPI()

class TestAppMain:
    """Tests for the main application functionality."""
    
    def test_should_create_task_with_valid_input(self):
        """Test creating a task with valid input."""
        # Arrange
        user_input = {"url": "https://example.com"}
        
        # Act
        response = app.post("/create_task", json=user_input)
        
        # Assert
        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert 'task_id' in response.json()
    
    def test_should_raise_error_with_invalid_input(self):
        """Test raising error with invalid input."""
        # Arrange
        user_input = {"url": "invalid_url"}
        
        # Act
        with pytest.raises(HTTPException) as exc_info:
            app.post("/create_task", json=user_input)
        
        # Assert
        assert exc_info.value.status_code == 422
    
    def test_should_get_task_status(self):
        """Test getting task status."""
        # Arrange
        user_input = {"url": "https://example.com"}
        response = app.post("/create_task", json=user_input)
        task_id = response.json()['task_id']
        
        # Act
        result = app.get(f"/get_task/{task_id}")
        
        # Assert
        assert result.status_code == 200
        assert isinstance(result.json(), dict)
        assert 'status' in result.json()
    
    def test_should_handle_task_not_found(self):
        """Test handling task not found."""
        # Arrange
        non_existent_task_id = "non_existent_task_id"
        
        # Act
        with pytest.raises(HTTPException) as exc_info:
            app.get(f"/get_task/{non_existent_task_id}")
        
        # Assert
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_async_task_creation(self):
        """Test asynchronous task creation."""
        # Arrange
        user_input = {"url": "https://example.com"}
        
        # Act
        response = await app.post("/create_task", json=user_input)
        task_id = response.json()['task_id']
        
        # Assert
        assert isinstance(response.json(), dict)
        assert 'task_id' in response.json()
    
    @pytest.mark.asyncio
    async def test_async_task_status(self):
        """Test asynchronous task status."""
        # Arrange
        user_input = {"url": "https://example.com"}
        response = await app.post("/create_task", json=user_input)
        task_id = response.json()['task_id']
        
        # Act
        result = await app.get(f"/get_task/{task_id}")
        
        # Assert
        assert isinstance(result.json(), dict)
        assert 'status' in result.json()
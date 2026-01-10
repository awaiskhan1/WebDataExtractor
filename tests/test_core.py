import pytest
from typing import Any, List

class TestCoreService:
    """Tests for Core Service functionality."""
    
    def test_should_extract_data_from_website(self):
        """Test data extraction from a website."""
        # Arrange
        url = "https://example.com"
        
        # Act
        result = extract_data(url)
        
        # Assert
        assert isinstance(result, dict)
        assert 'title' in result
        assert 'content' in result
    
    def test_should_handle_empty_url(self):
        """Test handling an empty URL."""
        with pytest.raises(ValueError) as exc_info:
            extract_data("")
        
        assert str(exc_info.value) == "URL cannot be empty"
    
    def test_should_handle_invalid_url(self):
        """Test handling an invalid URL."""
        with pytest.raises(ValueError) as exc_info:
            extract_data("invalid-url")
        
        assert str(exc_info.value) == "Invalid URL format"
    
    def test_should_filter_out_unwanted_content(self):
        """Test filtering out unwanted content."""
        url = "https://example.com"
        
        # Act
        result = extract_data(url, exclude_keywords=["ads", "footer"])
        
        # Assert
        assert 'title' in result
        assert 'content' not in result['content']
    
    def test_should_validate_extracted_data(self):
        """Test data validation."""
        url = "https://example.com"
        
        # Act
        result = extract_data(url)
        
        # Assert
        assert isinstance(result, dict)
        assert 'title' in result
        assert 'content' in result
        assert validate_data(result) is True
    
    def test_should_handle_validation_error(self):
        """Test handling validation error."""
        url = "https://example.com"
        
        # Act and Assert
        with pytest.raises(ValueError) as exc_info:
            extract_data(url, validate=False)
        
        assert str(exc_info.value) == "Data validation failed"

@pytest.mark.asyncio
async def test_async_extract_data(self):
    """Test async data extraction."""
    url = "https://example.com"
    
    result = await async_extract_data(url)
    
    assert isinstance(result, dict)
    assert 'title' in result
    assert 'content' in result
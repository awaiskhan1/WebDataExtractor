import pytest
from pydantic import ValidationError
from app.models.schemas import ExtractRequest, ExtractResponse, OrganizeRequest, OrganizeResponse

class TestExtractSchemas:
    """Tests for Extract schema functionality."""
    
    def test_extract_request_with_valid_data(self):
        """Test with valid extract request data."""
        request = ExtractRequest(url="https://example.com", extract_type="text")
        assert request.url == "https://example.com"
        assert request.extract_type == "text"

    def test_extract_request_with_default_type(self):
        """Test extract request with default type."""
        request = ExtractRequest(url="https://example.com")
        assert request.extract_type == "text"

    def test_extract_response_success(self):
        """Test successful extract response."""
        response = ExtractResponse(success=True, output="Extracted data")
        assert response.success is True
        assert response.output == "Extracted data"

    def test_extract_response_failure(self):
        """Test failed extract response."""
        response = ExtractResponse(success=False, error="Failed to extract")
        assert response.success is False
        assert response.error == "Failed to extract"

class TestOrganizeSchemas:
    """Tests for Organize schema functionality."""
    
    def test_organize_request_with_valid_data(self):
        """Test with valid organize request data."""
        request = OrganizeRequest(data="test data", format="json")
        assert request.data == "test data"
        assert request.format == "json"

    def test_organize_response_success(self):
        """Test successful organize response."""
        response = OrganizeResponse(success=True, output='{"data": "organized"}')
        assert response.success is True
        assert response.output == '{"data": "organized"}'
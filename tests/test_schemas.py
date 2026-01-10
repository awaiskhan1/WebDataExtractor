import pytest
from pydantic import ValidationError
from app.models.schemas import User, Product

class TestUserSchema:
    """Tests for User schema functionality."""
    
    def test_user_with_valid_data(self):
        """Test with valid user data."""
        input_data = {
            "id": 1,
            "username": "john_doe",
            "email": "john.doe@example.com"
        }
        
        user = User(**input_data)
        assert user.id == 1
        assert user.username == "john_doe"
        assert user.email == "john.doe@example.com"

    def test_user_with_missing_required_field(self):
        """Test with missing required field."""
        input_data = {
            "username": "john_doe",
            "email": "john.doe@example.com"
        }
        
        with pytest.raises(ValidationError) as e:
            User(**input_data)
        assert "id" in str(e.value)

    def test_user_with_invalid_email(self):
        """Test with invalid email format."""
        input_data = {
            "id": 1,
            "username": "john_doe",
            "email": "invalid-email"
        }
        
        with pytest.raises(ValidationError) as e:
            User(**input_data)
        assert "email" in str(e.value)

class TestProductSchema:
    """Tests for Product schema functionality."""
    
    def test_product_with_valid_data(self):
        """Test with valid product data."""
        input_data = {
            "id": 1,
            "name": "Laptop",
            "price": 999.99,
            "description": "High-performance laptop"
        }
        
        product = Product(**input_data)
        assert product.id == 1
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.description == "High-performance laptop"

    def test_product_with_missing_required_field(self):
        """Test with missing required field."""
        input_data = {
            "name": "Laptop",
            "price": 999.99,
            "description": "High-performance laptop"
        }
        
        with pytest.raises(ValidationError) as e:
            Product(**input_data)
        assert "id" in str(e.value)

    def test_product_with_negative_price(self):
        """Test with negative price."""
        input_data = {
            "id": 1,
            "name": "Laptop",
            "price": -100.00,
            "description": "High-performance laptop"
        }
        
        with pytest.raises(ValidationError) as e:
            Product(**input_data)
        assert "price" in str(e.value)
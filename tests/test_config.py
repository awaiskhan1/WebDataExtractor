import pytest
from typing import Any

class TestConfig:
    """Tests for Config functionality."""
    
    def test_should_load_default_configuration(self):
        """Test that default configuration is loaded correctly."""
        # Arrange
        from app.config import load_config
        
        # Act
        config = load_config()
        
        # Assert
        assert isinstance(config, dict)
        assert 'database_url' in config
        assert 'redis_host' in config
        assert 'pinecone_api_key' in config
    
    def test_should_load_custom_configuration(self):
        """Test that custom configuration is loaded correctly."""
        # Arrange
        from app.config import load_config
        
        custom_env = {
            'DATABASE_URL': 'postgresql://user:password@localhost/db',
            'REDIS_HOST': 'localhost',
            'PINECONE_API_KEY': 'api_key'
        }
        
        with pytest.MonkeyPatch.context() as monkeypatch:
            for key, value in custom_env.items():
                monkeypatch.setenv(key, value)
            
            # Act
            config = load_config()
            
            # Assert
            assert isinstance(config, dict)
            assert config['database_url'] == 'postgresql://user:password@localhost/db'
            assert config['redis_host'] == 'localhost'
            assert config['pinecone_api_key'] == 'api_key'
    
    def test_should_default_to_environment_variables(self):
        """Test that environment variables are used if no configuration file is provided."""
        # Arrange
        from app.config import load_config
        
        custom_env = {
            'DATABASE_URL': 'postgresql://user:password@localhost/db',
            'REDIS_HOST': 'localhost',
            'PINECONE_API_KEY': 'api_key'
        }
        
        with pytest.MonkeyPatch.context() as monkeypatch:
            for key, value in custom_env.items():
                monkeypatch.setenv(key, value)
            
            # Act
            config = load_config()
            
            # Assert
            assert isinstance(config, dict)
            assert config['database_url'] == 'postgresql://user:password@localhost/db'
            assert config['redis_host'] == 'localhost'
            assert config['pinecone_api_key'] == 'api_key'
    
    def test_should_fail_with_missing_environment_variables(self):
        """Test that an error is raised if required environment variables are missing."""
        # Arrange
        from app.config import load_config
        
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.delenv('DATABASE_URL')
            
            # Act & Assert
            with pytest.raises(EnvironmentError) as e:
                config = load_config()
    
    def test_should_handle_empty_configuration_file(self):
        """Test that an error is raised if the configuration file is empty."""
        # Arrange
        from app.config import load_config
        
        with open('app/config.py', 'w') as f:
            pass  # Empty file
        
        # Act & Assert
        with pytest.raises(ValueError) as e:
            config = load_config()
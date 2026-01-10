from pydantic import BaseModel, Field, SecretStr

class DatabaseSettings(BaseModel):
    database_url: str = Field(..., env='DATABASE_URL', description="The URL of the database")

class APISettings(BaseModel):
    ollama_api_key: SecretStr = Field(..., env='OLLAMA_API_KEY', description="API key for Ollama service")
    openai_api_key: SecretStr = Field(..., env='OPENAI_API_KEY', description="API key for OpenAI service")

class Settings(BaseModel):
    database: DatabaseSettings
    apis: APISettings

    @classmethod
    def load(cls) -> 'Settings':
        return cls.model_validate({
            "database": {
                "database_url": str(os.getenv('DATABASE_URL')),
            },
            "apis": {
                "ollama_api_key": SecretStr(str(os.getenv('OLLAMA_API_KEY'))),
                "openai_api_key": SecretStr(str(os.getenv('OPENAI_API_KEY'))),
            }
        })

settings = Settings.load()
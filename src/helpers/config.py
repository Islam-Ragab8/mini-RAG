from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 
    FILE_ALLOWED_TYPES: list
    MAX_FILE_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    class Config:
        env_file = env_file = ".env"
def get_settings() -> Settings:
    return Settings()
    
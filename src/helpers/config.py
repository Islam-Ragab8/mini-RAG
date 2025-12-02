from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 
    FILE_ALLOWED_TYPES: list
    MAX_FILE_SIXE: int

    class Config:
        env_file = ".env"
def get_settings() -> Settings:
    return Settings()
    
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cognitive Math Twin"
    API_V1: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./cognitive_math.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    MODEL_PATH: str = "./models/"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DYNAMODB_REGION: str
    OPENAI_API_KEY: str
    DEBUG: bool = False
    SESSION_SECRET_KEY: str
    USER_TABLE_NAME: str
    BUSINESS_TABLE_NAME: str
    BUSINESS_SURVEY_TABLE_NAME: str
    SURVEY_RECORD_TABLE_NAME: str

    class Config:
        env_file = ".env"


# This will autoload environment variables and you can access them via settings.DATABASE_URL, etc.
settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import Any
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DYNAMODB_REGION: str
    OPENAI_API_KEY: str
    DEBUG: bool = False
    SESSION_SECRET_KEY: str
    USER_TABLE_NAME: str
    BUSINESS_TABLE_NAME: str
    BUSINESS_SURVEY_TABLE_NAME: str
    SURVEY_RECORD_TABLE_NAME: str
    TEMPLATE_TABLE_NAME: str
    USERPOOL_REGION: str
    USERPOOL_ID: str
    APP_CLIENT_ID: str
    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    userpools: dict[str, dict[str, Any]] = {
            "us": {
                "region": os.getenv('USERPOOL_REGION'),
                "userpool_id": os.getenv('USERPOOL_ID'),
                "app_client_id": os.getenv('APP_CLIENT_ID')
            },
        }

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

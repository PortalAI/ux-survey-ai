from fastapi_cognito import CognitoAuth, CognitoSettings
from config import settings as config_setting


cognito_us = CognitoAuth(
  settings=CognitoSettings.from_global_settings(config_setting), userpool_name="us"
)

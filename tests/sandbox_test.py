import boto3
from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)

client_id = 'hheer4rr90ms4hk8d32tepc2b'
header = None
business_id = None
survey_id = None
record_id = None
headers = None
cognito_client = boto3.client('cognito-idp', region_name='us-west-2')


@pytest.fixture
def auth_token():
    response = cognito_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': 's@portal.ai',
            'PASSWORD': 'NhrY3rY5hLKF6R6r.',
        },
        ClientId=client_id,
    )
    return response['AuthenticationResult']['AccessToken']


def test_get_survey_info(auth_token):
    survey_id = 'fc67b07e9e284718bcb23ed925e3fd05'

    global headers, business_id
    headers = {
        'Authorization': f'Bearer {auth_token}',
    }
    response = client.get(
        f'/survey_info/{survey_id}',
        headers=headers
    )

    print(response.json())

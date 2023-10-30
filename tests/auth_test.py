
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
            'PASSWORD': '',
        },
        ClientId=client_id,
    )
    return response['AuthenticationResult']['AccessToken']

def test_create_business(auth_token):
    global headers, business_id
    headers = {
        'Authorization': f'Bearer {auth_token}',
    }
    
    # 1. create a business and get the business id
    business_name = "skins.cash"
    business_description = """
    Skins.cash is a website that allows users to sell their CS:GO skins for real money. It is one of the most popular websites for selling CS:GO skins, and it is known for its fast and easy transactions.
    To sell CS:GO skins on Skins.cash, users simply need to create an account and link their Steam account. Once their Steam account is linked, they can select the skins they want to sell and receive an offer from Skins.cash. If the user accepts the offer, they will need to trade the skins to Skins.cash. Once the skins are traded, Skins.cash will send the user their payment via PayPal, Skrill, or Bitcoin.
    Skins.cash is a legitimate website, and it has a good reputation among CS:GO players. However, it is important to note that all websites that buy and sell CS:GO skins come with some risk. It is always important to do your research before using any website to sell your skins.
    Here are some of the pros and cons of using Skins.cash:
    Pros:
    Fast and easy transactions
    Competitive prices
    Wide range of payment options
    Good reputation among CS:GO players
    """
    business_info = client.post(
        "/business/",
        headers=headers,
        json={
            "business_name": business_name,
            "business_description": business_description,
        }
    )

    business_id = business_info.json()['business_id']
    assert business_id is not None


def test_craete_survey():
    global survey_id
    survey_name = "User needs and preference"
    survey_description = """
    Your task is to engage the customer in a one-on-one interview,
    asking them questions to understand their needs and preferences
    in appropriate to your role and company style.
    The goal is to get valuable information to improve the service
    performance and effectiveness for the customer and service owners.
    """
    survey_info = client.post(
        "/survey/",
        headers=headers,
        json={
            "business_id": business_id,
            "survey_name": survey_name,
            "survey_description": survey_description
        }
    )
    survey_id = survey_info.json()['survey_id']
    assert survey_id is not None

def test_create_record():
    global record_id
    survey_record_info = client.post(
        "/survey_record/",
        headers=headers,
        json={
            "business_id": business_id,
            "survey_id": survey_id,
        }
    )

    record_id = survey_record_info.json()['record_id']
    assert record_id is not None

# def test_start_chat():
#     chat_response = client.post(
#         "/chat/",
#         headers=headers,
#         json={
#             "record_id": record_id,
#             "survey_id": survey_id,
#             "message": {
#                 "role": "human",
#                 "content": "Hi who are you?"
#             }
#         }
#     )

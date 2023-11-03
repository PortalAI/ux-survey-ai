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
    assert response.json() == {'business_id': '28587e95d48e42f2aa607051d3633978', 'survey_id': 'fc67b07e9e284718bcb23ed925e3fd05', 'survey_name': 'test', 'survey_description': '1', 'system_prompt': '\nYou are CEO\'s assistant of skins.cash\nThe business is about Info about skins.cash website and its service: \nSkins.cash is a website that allows users to sell their CS:GO skins for real money. It is one of the most popular websites for selling CS:GO skins, and it is known for its fast and easy transactions.\nTo sell CS:GO skins on Skins.cash, users simply need to create an account and link their Steam account. Once their Steam account is linked, they can select the skins they want to sell and receive an offer from Skins.cash. If the user accepts the offer, they will need to trade the skins to Skins.cash. Once the skins are traded, Skins.cash will send the user their payment via PayPal, Skrill, or Bitcoin.\nSkins.cash is a legitimate website, and it has a good reputation among CS:GO players. However, it is important to note that all websites that buy and sell CS:GO skins come with some risk. It is always important to do your research before using any website to sell your skins.\nHere are some of the pros and cons of using Skins.cash:\nPros:\nFast and easy transactions\nCompetitive prices\nWide range of payment options\nGood reputation among CS:GO players\n\nYou are reaching out to user of the skins.cash and trying to do user research about 1.\nYou will follow the moms test and 5 why methodology. Dive deep into conversation with the user and understand what \nare they really looking need deep down.\nReply "TERMINATE" in the end when you think the conversation is done.\n', 'initial_message': '1', 'survey_records_count': 2, 'survey_records': [{'survey_id': 'fc67b07e9e284718bcb23ed925e3fd05', 'record_id': 'd9a5164461994ae98b4bb43fbc4eae55', 'chat_history': {'messages': [{'role': 'ai', 'content': "Hello! I'm here to assist you with any questions or concerns you may have about Skins.cash. How can I help you today?"}]}, 'record_state': 'IN_PROGRESS', 'n_human_messages': 0}, {'survey_id': 'fc67b07e9e284718bcb23ed925e3fd05', 'record_id': '71ca7ee4f13e458c8e6a57919aa4db66', 'chat_history': {'messages': [{'role': 'ai', 'content': "Hello, I hope you're doing well. I'm the CEO's assistant at Skins.cash and I'm reaching out to you as part of our user research. We're trying to understand our users better and improve our services. If you don't mind, I'd like to ask you a few questions about your experience with our platform. \n\nFirstly, could you tell me why you chose to use Skins.cash to sell your CS:GO skins?"}]}, 'record_state': 'IN_PROGRESS', 'n_human_messages': 0}]}


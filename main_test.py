from fastapi.testclient import TestClient
import pytest


from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health_check")
    
    assert response.status_code == 200
    assert response.json() == {"message": "server is healthy"}

# Business
def test_create_business():
    response = client.post(
        "/business/",
        headers={"X-Token": "coneofsilence"},
        json={"business_name": "test biz name", "business_description": "test biz description"},
    )
    assert response.status_code == 200
    assert response.json().get("business_name") == "test biz name"
    assert response.json().get("business_description") == "test biz description"

def test_update_business():
    biz_name = "test biz new name"
    biz_desc = "test biz new description"
    response = client.put(
        "/business/",
        headers={"X-Token": "coneofsilence"},
        json={
            "business_id":"cef8ea0129c7468da7d5374c4a0ea4bc",
            "business_name": biz_name,
            "business_description": biz_desc
        },
    )
    assert response.status_code == 200
    assert response.json().get("business_name") == biz_name
    assert response.json().get("business_description") == biz_desc

def test_get_business():
    response = client.get(
        "/business/cef8ea0129c7468da7d5374c4a0ea4bc",
    )
    assert response.status_code == 200
    assert response.json().get("business_name") == "test biz new name"

# Survey
def test_create_survey():
    response = client.post(
        "/survey/",
        json={
            "business_id": "cef8ea0129c7468da7d5374c4a0ea4bc",
            "survey_name": "test_survey",
            "survey_description": "test survey desc",
            "initial_message": "random random",
        }
    )
    assert response.status_code == 200
    assert response.json().get("initial_message") == "random random"


def test_end_2_end_happy_path():
    # 1. create a business and get the business id
    business_name = "Sam's welding corporation"
    business_description = "The business is help young profession who can't find a job to be more strong and weld more iron!"
    business_info = client.post(
        "/business/",
        json={
            "business_name": business_name,
            "business_description": business_description,
        }
    )
    business_id = business_info.json()['business_id']
    # 1.1 verify the business created above by getting it.
    retrieved_business_info = client.get(
        f"/business/{business_id}"
    )
    assert retrieved_business_info.json()["business_id"] == business_id
    assert retrieved_business_info.json()["business_name"] == business_name
    assert retrieved_business_info.json()["business_description"] == business_description
    # 2. create a survey with business id and get the survey id
    survey_name = "User job security"
    survey_description = "getting to know how our customer welding practice make them more confident and if they have landed a job. if not find out why."
    survey_info = client.post(
        "/survey/",
        json={
            "business_id": business_id,
            "survey_name": survey_name,
            "survey_description": survey_description
        }
    )
    survey_id = survey_info.json()['survey_id']
    # 2.2 verify the survey created above by getting it.
    retrieved_survey_info = client.get(
        f"/survey/{survey_id}"
    )
    assert retrieved_survey_info.json()["survey_id"] == survey_id
    assert retrieved_survey_info.json()["survey_name"] == survey_name
    assert retrieved_survey_info.json()["survey_description"] == survey_description
    # 3. create a survey record with business id and survey id
    survey_record_info = client.post(
        "/survey_record/",
        json={
            "business_id": business_id,
            "survey_id": survey_id,
            "survey_description": "getting to know how our customer welding practice make them more confident and if they have landed a job. if not find out why."
        }
    )

    record_id = survey_record_info.json()['record_id']
    print(f"got {survey_record_info.json()}")
    # 4. start a conversation using the record id survey id
    chat_response = client.post(
        "/chat/",
        json={
            "record_id": record_id,
            "survey_id": survey_id,
            "message": {
                "role": "human",
                "content": "Hi who are you?"
            }
        }
    )
    print(f"got {chat_response.json()}")



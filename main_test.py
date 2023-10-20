from fastapi.testclient import TestClient
from fastapi import status
from agent import prompt_templates
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health_check")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "server is healthy"}


# Business
def test_create_business():
    response = client.post(
        "/business/",
        headers={"X-Token": "coneofsilence"},
        json={"business_name": "test biz name", "business_description": "test biz description"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.pop("business_id")  # check if business_id is returned
    assert data == {
        "business_name": "test biz name",
        "business_description": "test biz description"
    }


def test_update_business():
    update_data = {
        "business_id": "cef8ea0129c7468da7d5374c4a0ea4bc",
        "business_name": "test biz new name",
        "business_description": "test biz new description"
    }
    response = client.put(
        "/business/",
        headers={"X-Token": "coneofsilence"},
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == update_data


def test_get_business():
    response = client.get(
        "/business/1",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("business_name") == "Mike's welding corporation"


# Survey
def test_create_survey():
    response = client.post(
        "/survey/",
        json={
            "business_id": "1",
            "survey_name": "test_survey",
            "survey_description": "test survey desc",
            "initial_message": "random random",
        }
    )
    assert response.status_code == status.HTTP_200_OK
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
    # 4.1 send a second chat
    chat_response = client.post(
        "/chat/",
        json={
            "record_id": record_id,
            "survey_id": survey_id,
            "message": {
                "role": "human",
                "content": "How can I help you?"
            }
        }
    )
    print(f"got {chat_response.json()}")

    # 5. check chat history from get_history
    chat_history_response = client.get(f"/chat_history/{record_id}")

    print(f"get chat history got {chat_history_response.json()['chat_history']}")
    # 6. check chat history from survey_record post endpoint
    survey_record_info = client.post(
        "/survey_record/",
        json={
            "record_id": record_id,
            "business_id": business_id,
            "survey_id": survey_id,
        }
    )
    print(f"post survey_record got {survey_record_info.json()['chat_history']}")


def test_get_surveys_by_business_id():
    surveys = client.get(
        "/business/1/survey"
    )
    print(surveys.json())


def test_get_chat_history():
    chat_history = client.get(
        "/chat_history/b5f96a01186d4b57978a61dc22934c1d"
    )
    print(chat_history.json())


def test_record_summary_dummy():
    record_summary = client.get(
        "/survey_record/1/summary"
    )
    assert record_summary.json().get("chat_summary") == "dummy chat summary, not implemented"


def test_survey_insight_dummy():
    survey_insight = client.get(
        "/survey/1/insight"
    )
    assert survey_insight.json().get("survey_insight") == "dummy response, not implemented yet"


def test_list_survey_records():
    survey_records = client.get(
        "/survey/95abd0de16d848109d50f6967b24718f/records"
    )
    print(survey_records.json())


def test_cached_chat():
    survey_record_info = client.post(
        "/survey_record/",
        json={
            "business_id": "cc103440e63c49488fe2b4e177ab7452",
            "survey_id": "95abd0de16d848109d50f6967b24718f",
            "survey_description": "getting to know how our customer welding practice make them more confident and if they have landed a job. if not find out why."
        }
    )

    record_id = survey_record_info.json()['record_id']
    print(f"got {survey_record_info.json()}")
    survey_record_info = client.post(
        "/survey_record/",
        json={
            "record_id": record_id,
            "business_id": "cc103440e63c49488fe2b4e177ab7452",
            "survey_id": "95abd0de16d848109d50f6967b24718f",
            "survey_description": "getting to know how our customer welding practice make them more confident and if they have landed a job. if not find out why."
        }
    )
    print(f"got {survey_record_info.json()['chat_history']}")


def test_create_template():
    response = client.post(
        '/template/',
        json={
            # todo make sure survey id is present in the db
            "survey_id": "1",
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.pop("template_id")  # check if template_id is returned
    assert data == {
        "survey_id": "1",
        'system_message': prompt_templates.SYSTEM_MESSAGE,
        'system_message_params': prompt_templates.SYSTEM_MESSAGE_PARAMS,
        'agent_initial_message': prompt_templates.AGENT_INITIAL_MESSAGE,
        'agent_initial_message_params': prompt_templates.AGENT_INITIAL_MESSAGE_PARAMS,
        'summary_single_prompt': prompt_templates.SUMMARY_SINGLE_PROMPT,
        'summary_single_prompt_params': prompt_templates.SUMMARY_SINGLE_PROMPT_PARAMS,
        'get_insight_prompt': prompt_templates.GET_INSIGHT_PROMPT,
        'get_insight_prompt_params': prompt_templates.GET_INSIGHT_PROMPT_PARAMS,
    }
    # todo does test actually create a template in the db?


def test_update_template():
    update_data = {
        "template_id": "7e6af56c90524f149362d2379caf2d04",
        "survey_id": "1",
        "system_message": "new system message",
        "system_message_params": ["new system message params"],
        "agent_initial_message": "new agent initial message",
        "agent_initial_message_params": ["new agent initial message params"],
        "summary_single_prompt": "new summary single prompt",
        "summary_single_prompt_params": ["new summary single prompt params"],
        "get_insight_prompt": "new get insight prompt",
        "get_insight_prompt_params": ["new get insight prompt params"],
    }
    response = client.put(
        '/template/',
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == update_data


def test_get_template():
    # from previous test
    response = client.get(
        "/template/7e6af56c90524f149362d2379caf2d04",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('system_message') == "new system message"

    # not found
    assert client.get("/template/1").status_code == status.HTTP_404_NOT_FOUND


def test_get_template_by_survey_id():
    client.post("template/", json={"survey_id": "1"})

    response = client.get("/survey/1/template")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('system_message') == prompt_templates.SYSTEM_MESSAGE

    # not found
    assert client.get("/survey/2/template").status_code == status.HTTP_404_NOT_FOUND

# TODO: add test for load message from db
# todo there has to be internal error logging for each request

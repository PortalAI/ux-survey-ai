from fastapi.testclient import TestClient



from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health_check")
    
    assert response.status_code == 200
    assert response.json() == {"message": "server is healthy"}

# Business
def test_create_business():
    response = client.post(
        "/create_business/",
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
        "/update_business/",
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
        "/create_survey/",
        json={
            "business_id": "cef8ea0129c7468da7d5374c4a0ea4bc",
            "survey_name": "test_survey",
            "survey_description": "test survey desc",
            "initial_message": "random random",
        }
    )
    assert response.status_code == 200
    assert response.json().get("initial_message") == "random random"

import requests

expected_schema = {
    "uuid": str,
    "historyId": str,
    "fullName": str,
    "labels": list,
    "links": list,
    "name": str,
    "status": str,
    "statusDetails": dict,
    "stage": str,
    "description": str,
    "steps": list
}

BASE_URL = 'https://flask-rest-api-ysf4.onrender.com'


def test_allure_health_get_all():
    endpoint = f'{BASE_URL}/jsons'
    response = requests.get(endpoint)
    assert response.status_code == 200


def test_create_record_success():
    payload = {
        "uuid": "test-uuid",
        "historyid": "test-history-id",
        "fullname": "Test Full Name",
        "labels": {"label1": "value1"},
        "name": "Test Name",
        "status": "passed",
        "statusdetails": {"detail1": "value1"},
        "stage": "completed",
        "description": "Test Description",
        "steps": [{"step1": "action1"}],
        "attachments": [{"type": "image", "url": "http://example.com/image.png"}],
        "parameters": {"param1": "value1"},
        "start": 1234567890,
        "stop": 1234567891
    }

    response = create_record(payload)
    # assert response.status_code == 201
    # response_json = response.json()
    # assert response_json["message"] == "Record created"
    # assert response_json["uuid"] == "test-uuid"


def create_record(data):
    return requests.post(BASE_URL, json=data)

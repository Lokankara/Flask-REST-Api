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

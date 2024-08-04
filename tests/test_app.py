import json

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
    "steps": list
}

# BASE_URL = 'https://flask-rest-api-ysf4.onrender.com'
BASE_URL = 'http://127.0.0.1:5000'


def test_allure_health_get_all():
    endpoint = f'{BASE_URL}/jsons'
    response = requests.get(endpoint)
    assert response.status_code == 200


def test_create_record_success():
    url = BASE_URL + '/json'

    with open('json/post.json', 'r') as file:
        payload = json.load(file)

    response = requests.post(url, json=payload)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"


def test_delete_record_success():
    url = f'{BASE_URL}/json'

    with open('json/post.json', 'r') as file:
        uuid = json.load(file)["uuid"]

    response = requests.delete(f'{url}/{uuid}')

    assert response.status_code != 500, f"Expected status code to be not 500, but got {response.status_code}"
    assert response.status_code == 200

    response_check = requests.get(f'{url}/{uuid}')
    assert response_check.status_code == 404

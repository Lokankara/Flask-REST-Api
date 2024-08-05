import os
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

BASE_URL = 'https://flask-rest-api-ysf4.onrender.com'


def test_allure_health_get_all():
    endpoint = f'{BASE_URL}/results'
    response = requests.get(endpoint)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"


def test_create_record_success():
    url = BASE_URL + '/result'
    print("Current Working Directory:", os.getcwd())

    file_path = os.path.join(os.path.dirname(__file__), 'json', 'post.json')

    with open(file_path, 'r') as file:
        payload = json.load(file)

    response = requests.post(url, json=payload)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"


def test_delete_record_success():
    url = f'{BASE_URL}/result'

    file_path = os.path.join(os.path.dirname(__file__), 'json', 'post.json')
    with open(file_path, 'r') as file:
        uuid = json.load(file)['uuid']

    response = requests.delete(f'{url}/{uuid}')

    assert response.status_code != 500, f"Expected status code to be not 500, but got {response.status_code}"
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    response_check = requests.get(f'{url}/{uuid}')
    assert response_check.status_code == 404

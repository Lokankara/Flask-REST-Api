import os
from datetime import datetime

import pytz
import json
import requests


def get_json_data(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'json', filename)
    with open(file_path, 'r') as file:
        return json.load(file)


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


# BASE_URL = 'http://127.0.0.1:5000'
BASE_URL = 'https://flask-rest-api-ysf4.onrender.com'

results = f'{BASE_URL}/results'
result_url = f'{BASE_URL}/result'


# @pytest.fixture(scope='module')
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#
#     with app.app_context():
#         db.create_all()
#
#     with app.test_client() as client:
#         yield client
#
#     with app.app_context():
#         db.drop_all()


def test_get_all_results():
    response = requests.get(results)
    assert response.status_code == 200


def test_create_result():
    payload = get_json_data('result.json')
    response = requests.post(result_url, json=payload)

    assert response.status_code == 201
    assert response.json()['uuid'] == payload['uuid']


def test_get_result():
    payload = get_json_data('result.json')
    url = f'{BASE_URL}/result/{payload["uuid"]}'
    response = requests.get(url)
    assert response.status_code == 200

    deep_compare(response.json(), payload)


def test_delete_result():
    payload = get_json_data('result.json')
    uuid = payload["uuid"]
    url = f'{BASE_URL}/result/{uuid}'
    response = requests.delete(url)

    assert response.status_code == 200
    assert response.json()['message'] == 'Record deleted'

    response = requests.get(result_url)
    assert response.status_code == 405


def test_allure_health_get_all():
    response = requests.get(results)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"


def test_create_record_success():
    payload = get_json_data('result.json')
    response = requests.post(result_url, json=payload)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"


def test_delete_record_success():
    uuid = get_json_data('result.json')['uuid']
    response = requests.delete(f'{result_url}/{uuid}')

    assert response.status_code != 500, f"Expected status code to be not 500, but got {response.status_code}"
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    response_check = requests.get(f'{result_url}/{uuid}')
    assert response_check.status_code == 404


def deep_compare(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        for key in a:
            if key not in b:
                return False
            if not deep_compare(a[key], b[key]):
                return False
        for key in b:
            if key not in a:
                return False
        return True
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        for n, m in zip(a, b):
            if not deep_compare(n, m):
                return False
        return True
    elif isinstance(a, str) and isinstance(b, str):
        return transform(a) == transform(b)
    else:
        return a == b


def transform(date_string):
    return int(datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S GMT')
               .replace(tzinfo=pytz.UTC).timestamp() * 1000)

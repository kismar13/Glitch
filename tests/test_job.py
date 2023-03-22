import json
from random import random

import requests


def main_job():
    test_all_jobs()
    test_job_1()
    test_job_not_found()
    test_job_str()


BASE_URL = 'http://localhost:5000/api'


def test_all_jobs() -> None:
    response = requests.get(f'{BASE_URL}/job')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_job_1() -> None:
    response = requests.get(f'{BASE_URL}/job/1')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_job_not_found() -> None:
    response = requests.get(f'{BASE_URL}/job/666')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_job_str() -> None:
    response = requests.get(f'{BASE_URL}/job/qwq')
    data = response.json()
    print(json.dumps(data, indent=4))


def test_add_job() -> None:
    response = requests.post(f'{BASE_URL}/jobs', json={
        'id': random.randint(1000, 10000),
        'job': 'installation of radiation protection',
        'team_leader': 1,
        'work_size': 45,
        'collaborators': '6, 4, 7',
        'is_finished': False,
    })
    data = response.json()
    print(json.dumps(data, indent=4))
    test_all_jobs()


def test_add_job_already_exists() -> None:
    response = requests.post(f'{BASE_URL}/jobs', json={
        'id': 1,
        'job': 'installation of radiation protection',
        'team_leader': 1,
        'work_size': 45,
        'collaborators': '6, 4, 7',
        'is_finished': False,
    })
    data = response.json()
    print(json.dumps(data, indent=4))
    test_all_jobs()



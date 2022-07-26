from http import HTTPStatus

import pytest
import requests


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_new_action_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(url_base + "access/action", headers=root_auth_headers, json={"name": "test_action"})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["message"] == "Action created."


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_existing_action_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(url_base + "access/action", headers=root_auth_headers, json={"name": "test_action"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_one_action_retrieving(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/action", headers=root_auth_headers, json={"id": 1})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["action"] == {"id": 1, "name": "role_create"}


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_existing_action_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/action", headers=root_auth_headers, json={"name": "test_action"})
    action_id = response.json()["action"]["id"]

    response = requests.delete(url_base + "access/action", headers=root_auth_headers, json={"id": action_id})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_missing_action_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.delete(url_base + "access/action", headers=root_auth_headers, json={"id": -1})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_get_user_actions(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "check/action", headers=root_auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["actions"] == [num for num in range(1, 16)]

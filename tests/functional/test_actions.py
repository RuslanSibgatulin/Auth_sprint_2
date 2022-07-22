import pytest
import requests


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_new_action_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(url_base + "access/action", headers=root_auth_headers, params={"name": "test_action"})
    assert response.status_code == 201
    assert response.json()["message"] == "Action created."


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_existing_action_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(url_base + "access/action", headers=root_auth_headers, params={"name": "test_action"})
    assert response.status_code == 400


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_one_action_retrieving(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/action", headers=root_auth_headers, params={"id": 1})
    assert response.status_code == 200
    assert response.json()["action"] == {"id": 1, "name": "role_create"}


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_existing_action_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/action", headers=root_auth_headers, params={"name": "test_action"})
    action_id = response.json()["action"]["id"]

    response = requests.delete(url_base + "access/action", headers=root_auth_headers, params={"id": action_id})
    assert response.status_code == 200


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_missing_action_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.delete(url_base + "access/action", headers=root_auth_headers, params={"id": -1})
    assert response.status_code == 404

import pytest
import requests


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_existing_role_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(
        url_base + "access/role",
        headers=root_auth_headers,
        json={"name": "superuser", "actions": ["role_read", "action_read"]},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Role superuser already exists"


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_missing_actions_role_addition(root_auth_headers: dict[str, str], url_base: str):
    missing_actions = ",".join(["missing_action1", "missing_action2"])
    response = requests.post(
        url_base + "access/role",
        headers=root_auth_headers,
        json={"name": "test_role", "actions": missing_actions},
    )
    assert response.status_code == 400
    assert response.json()["message"] == f"Unknown actions: {missing_actions}"


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_role_addition(root_auth_headers: dict[str, str], url_base: str):
    response = requests.post(
        url_base + "access/role",
        headers=root_auth_headers,
        json={"name": "test_role", "actions": ["role_read", "action_read"]},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Role created."


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_missing_role_updating(root_auth_headers: dict[str, str], url_base: str):
    response = requests.put(
        url_base + "access/role",
        headers=root_auth_headers,
        json={"id": -1, "name": "role", "actions": "role_read"},
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Role with id -1 not found"


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_role_updating_missing_actions(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/role", headers=root_auth_headers, params={"name": "test_role"})
    action_id = response.json()["role"]["id"]

    missing_actions = ",".join(["missing_action1", "missing_action2"])
    response = requests.put(
        url_base + "access/role",
        headers=root_auth_headers,
        json={"id": action_id, "name": "test_role", "actions": missing_actions},
    )
    assert response.status_code == 400
    assert response.json()["message"] == f"Unknown actions: {missing_actions}"


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_missing_role_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.delete(url_base + "access/role", headers=root_auth_headers, params={"id": -1})
    assert response.status_code == 404


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_role_deletion(root_auth_headers: dict[str, str], url_base: str):
    response = requests.get(url_base + "access/role", headers=root_auth_headers, params={"name": "test_role"})
    action_id = response.json()["role"]["id"]

    response = requests.delete(url_base + "access/role", headers=root_auth_headers, params={"id": action_id})
    assert response.status_code == 200

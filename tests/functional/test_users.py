from http import HTTPStatus

import pytest
import requests


@pytest.mark.parametrize(
    "login,email,password,second_password,message,code",
    [
        ("user1", "email1@email.email", "1322", "1322", "User created.", HTTPStatus.CREATED),
        ("user3", "email3@email.ru", "1322", "13222", "Error! Check your passwords.", HTTPStatus.BAD_REQUEST),
        ("user2", "email2@email.ru", "1322", "1322", "User created.", HTTPStatus.CREATED),
        ("user2", "email3@email.ru", "1322", "1322", "Error! User with login - user2 already exists.", HTTPStatus.BAD_REQUEST),
        ("user3", "email2@email.ru", "1322", "1322", "Error! User with email - email2@email.ru already exists.", HTTPStatus.BAD_REQUEST),
    ],
)
@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_create_users(
    url_base: str, login: str, email: str, password: str, second_password: str, message: str, code: int
):
    response = requests.post(
        url_base + "sign-up",
        json={"login": login, "email": email, "password": password, "second_password": second_password},
    )
    assert response.status_code == code
    assert response.json()["message"] == message


@pytest.mark.parametrize(
    "login,password,message,code",
    [
        ("user2", "13222", "Wrong password", HTTPStatus.UNAUTHORIZED),
        ("user10", "1322", "User with login user10 does't exists.", HTTPStatus.NOT_FOUND),
        ("user2", "1322", None, HTTPStatus.OK),
    ],
)
@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_login_user(url_base: str, login: str, password: str, message: str, code: int):
    resp = requests.post(
        url_base + "login",
        json={
            "login": login,
            "password": password,
        },
    )
    assert resp.status_code == code
    resp_data = resp.json()
    if "message" in resp_data:
        assert resp_data["message"] == message
    else:
        assert len(resp_data) == 2
        assert bool("access_token" in resp_data) is True
        assert bool("refresh_token" in resp_data) is True


@pytest.mark.parametrize(
    "login,password,agent",
    [
        ("user1", "1322", "User Agent 1.0"),
        ("user1", "1322", "User Agent 2.0"),
    ],
)
@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_refresh_view(user_token_pair, url_base: str, login: str, password: str, agent: str):
    token_pair = user_token_pair(login, password, agent)
    refresh_token = token_pair.json()["refresh_token"]
    response = requests.post(
        url_base + "refresh", headers={"User-Agent": agent, "Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    token_pair = response.json()
    assert len(token_pair) == 2
    refresh_token_new = token_pair.get("refresh_token")
    access_token = token_pair.get("access_token")
    assert refresh_token is not None
    assert access_token is not None
    fake_response = requests.post(
        url_base + "refresh", headers={"User-Agent": "Fake Agent 1.0", "Authorization": f"Bearer {refresh_token_new}"}
    )
    assert fake_response.status_code == HTTPStatus.BAD_REQUEST
    assert fake_response.json()["message"] == "Refresh token has expired. Login again."


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_get_login_hisory(url_base: str, user_token_pair):
    token_pair = user_token_pair("user1", "1322", "User Agent 1.0")
    access_token = token_pair.json()["access_token"]
    response = requests.get(
        url_base + "history", headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["logins"]) == 3


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_user_logout(url_base: str, user_token_pair):
    token_pair_first = user_token_pair("user1", "1322", "User Agent 1.0")
    token_pair_second = user_token_pair("user1", "1322", "User Agent 2.0")
    access_token_first = token_pair_first.json()["access_token"]
    refresh_token_first = token_pair_first.json()["refresh_token"]
    access_token_second = token_pair_second.json()["access_token"]
    refresh_token_second = token_pair_second.json()["refresh_token"]
    response_logout = requests.post(
        url_base + "logout", headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token_first}"}
    )
    assert response_logout.status_code == HTTPStatus.OK
    assert response_logout.json()["message"] == "You logged out."

    response_refresh_first = requests.post(
        url_base + "refresh",
        headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {refresh_token_first}"},
    )
    assert response_refresh_first.status_code == HTTPStatus.BAD_REQUEST
    assert response_refresh_first.json()["message"] == "Refresh token has expired. Login again."

    response_history_first = requests.get(
        url_base + "history", headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token_first}"}
    )
    assert response_history_first.status_code == HTTPStatus.BAD_REQUEST
    assert response_history_first.json()["message"] == "Refresh your access token."

    response_history_second = requests.get(
        url_base + "history",
        headers={"User-Agent": "User Agent 2.0", "Authorization": f"Bearer {access_token_second}"},
    )
    assert response_history_second.status_code == HTTPStatus.OK
    assert len(response_history_second.json()["logins"]) == 5

    response_refresh_second = requests.post(
        url_base + "refresh",
        headers={"User-Agent": "User Agent 2.0", "Authorization": f"Bearer {refresh_token_second}"},
    )
    assert response_refresh_second.status_code == HTTPStatus.OK
    assert len(response_refresh_second.json()) == 2
    resp_data = response_refresh_second.json()
    assert bool("access_token" in resp_data) is True
    assert bool("refresh_token" in resp_data) is True


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_user_logout_all(url_base: str, user_token_pair):
    token_pair_first = user_token_pair("user1", "1322", "User Agent 1.0")
    token_pair_second = user_token_pair("user1", "1322", "User Agent 2.0")
    access_token_first = token_pair_first.json()["access_token"]
    refresh_token_first = token_pair_first.json()["refresh_token"]
    access_token_second = token_pair_second.json()["access_token"]
    refresh_token_second = token_pair_second.json()["refresh_token"]
    response_logout = requests.post(
        url_base + "logout-all",
        headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token_first}"},
    )
    assert response_logout.status_code == HTTPStatus.OK
    assert response_logout.json()["message"] == "You logged out."

    response_history_first = requests.get(
        url_base + "history", headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token_first}"}
    )
    assert response_history_first.status_code == HTTPStatus.BAD_REQUEST
    assert response_history_first.json()["message"] == "Refresh your access token."

    response_refresh_first = requests.post(
        url_base + "refresh",
        headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {refresh_token_first}"},
    )
    assert response_refresh_first.status_code == HTTPStatus.BAD_REQUEST
    assert response_refresh_first.json()["message"] == "Refresh token has expired. Login again."

    response_history_second = requests.get(
        url_base + "history",
        headers={"User-Agent": "User Agent 2.0", "Authorization": f"Bearer {access_token_second}"},
    )
    assert response_history_second.status_code == HTTPStatus.BAD_REQUEST
    assert response_history_first.json()["message"] == "Refresh your access token."

    response_refresh_second = requests.post(
        url_base + "refresh",
        headers={"User-Agent": "User Agent 2.0", "Authorization": f"Bearer {refresh_token_second}"},
    )
    assert response_refresh_second.status_code == HTTPStatus.BAD_REQUEST
    assert response_refresh_second.json()["message"] == "Refresh token has expired. Login again."


@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_user_two_sessions(url_base: str, user_token_pair):
    token_pair_first = user_token_pair("user1", "1322", "User Agent 1.0")
    token_pair_second = user_token_pair("user1", "1322", "User Agent 2.0")
    response_refresh_first = requests.post(
        url_base + "refresh",
        headers={
            "User-Agent": "User Agent 1.0",
            "Authorization": f"Bearer {token_pair_first.json()['refresh_token']}",
        },
    )
    response_refresh_second = requests.post(
        url_base + "refresh",
        headers={
            "User-Agent": "User Agent 2.0",
            "Authorization": f"Bearer {token_pair_second.json()['refresh_token']}",
        },
    )
    assert response_refresh_first.status_code == HTTPStatus.OK
    assert response_refresh_second.status_code == HTTPStatus.OK
    assert len(response_refresh_first.json()) == 2
    assert len(response_refresh_second.json()) == 2
    assert bool("refresh_token" in response_refresh_first.json()) is True
    assert bool("access_token" in response_refresh_first.json()) is True
    assert bool("refresh_token" in response_refresh_second.json()) is True
    assert bool("access_token" in response_refresh_second.json()) is True
    new_access_token_first = response_refresh_first.json()["access_token"]
    new_access_token_second = response_refresh_second.json()["access_token"]
    response_history_first = requests.get(
        url_base + "history",
        headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {new_access_token_first}"},
    )
    response_history_second = requests.get(
        url_base + "history",
        headers={"User-Agent": "User Agent 2.0", "Authorization": f"Bearer {new_access_token_second}"},
    )
    assert response_history_first.status_code == HTTPStatus.OK
    assert response_history_second.status_code == HTTPStatus.OK
    assert len(response_history_first.json()["logins"]) == 9
    assert len(response_history_second.json()["logins"]) == 9


@pytest.mark.parametrize(
    "login,password,new_login,new_password,code,message",
    [
        ("user1", "132222", "user10", "132222", HTTPStatus.BAD_REQUEST, "Wrong old password."),
        ("user1", "1322", "user2", "132222", HTTPStatus.BAD_REQUEST, "User with login user2 already exists."),
        ("user1", "1322", "user10", "132222", HTTPStatus.OK, "Your profile updated."),
    ],
)
@pytest.mark.parametrize("url_base", ["v1"], indirect=True)
def test_change_user(
    user_token_pair,
    url_base: str,
    login: str,
    password: str,
    new_login: str,
    new_password: str,
    code: int,
    message: str,
):
    token_pair = user_token_pair(login, "1322", "User Agent 1.0")
    access_token = token_pair.json()["access_token"]
    response = requests.put(
        url_base + "profile",
        json={"login": new_login, "password": new_password, "old_password": password},
        headers={"User-Agent": "User Agent 1.0", "Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == code
    assert response.json()["message"] == message
    if code == HTTPStatus.OK:
        token_pair = user_token_pair(new_login, new_password, "User Agent 1.0")
        assert token_pair.status_code == HTTPStatus.OK
        assert len(token_pair.json()) == 2
        tokens = token_pair.json()
        assert bool("access_token" in tokens) is True
        assert bool("refresh_token" in tokens) is True

import os

import pytest
import requests


@pytest.fixture(scope="session")
def url_base() -> str:
    host = os.getenv("API_HOST", None)
    port = os.getenv("API_PORT", None)
    if not host or not port:
        raise EnvironmentError("Both api_host and api_port must be defined")
    return f"http://{host}:{port}/v1/"


@pytest.fixture(scope="session")
def root_session_token(url_base: str) -> str:
    response = requests.post(url_base + "login", json={"login": "root", "password": "root"})
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def root_auth_headers(root_session_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {root_session_token}"}


@pytest.fixture(scope="session")
def user_token_pair(url_base: str):
    def inner(login: str, password: str, agent: str):
        response = requests.post(
            url_base + "login", json={"login": login, "password": password}, headers={"User-Agent": agent}
        )
        return response

    return inner

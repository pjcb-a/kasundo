import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_token(client):
    test_login = os.getenv("KASUNDO_TEST_LOGIN")
    test_password = os.getenv("KASUNDO_TEST_PASSWORD")

    if not test_login or not test_password:
        pytest.skip(
            "Set KASUNDO_TEST_LOGIN and KASUNDO_TEST_PASSWORD to run authenticated tests."
        )

    response = client.post(
        "/auth/login",
        json={
            "login": test_login,
            "password": test_password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture(scope="session")
def lender_token(client):
    test_login = os.getenv("KASUNDO_TEST_LENDER_LOGIN")
    test_password = os.getenv("KASUNDO_TEST_LENDER_PASSWORD")

    if not test_login or not test_password:
        pytest.skip(
            "Set KASUNDO_TEST_LENDER_LOGIN and KASUNDO_TEST_LENDER_PASSWORD."
        )

    response = client.post(
        "/auth/login",
        json={
            "login": test_login,
            "password": test_password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def borrower_token(client):
    test_login = os.getenv("KASUNDO_TEST_BORROWER_LOGIN")
    test_password = os.getenv("KASUNDO_TEST_BORROWER_PASSWORD")

    if not test_login or not test_password:
        pytest.skip(
            "Set KASUNDO_TEST_BORROWER_LOGIN and KASUNDO_TEST_BORROWER_PASSWORD."
        )

    response = client.post(
        "/auth/login",
        json={
            "login": test_login,
            "password": test_password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def lender_headers(lender_token):
    return {
        "Authorization": f"Bearer {lender_token}"
    }


@pytest.fixture(scope="session")
def borrower_headers(borrower_token):
    return {
        "Authorization": f"Bearer {borrower_token}"
    }


@pytest.fixture(scope="session")
def test_borrower_id():
    borrower_id = os.getenv("KASUNDO_TEST_BORROWER_ID")

    if not borrower_id:
        pytest.skip("Set KASUNDO_TEST_BORROWER_ID.")

    return int(borrower_id)


@pytest.fixture(scope="session")
def unrelated_token(client):
    test_login = os.getenv("KASUNDO_TEST_UNRELATED_LOGIN")
    test_password = os.getenv("KASUNDO_TEST_UNRELATED_PASSWORD")

    if not test_login or not test_password:
        pytest.skip(
            "Set KASUNDO_TEST_UNRELATED_LOGIN and KASUNDO_TEST_UNRELATED_PASSWORD."
        )

    response = client.post(
        "/auth/login",
        json={
            "login": test_login,
            "password": test_password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def unrelated_headers(unrelated_token):
    return {
        "Authorization": f"Bearer {unrelated_token}"
    }
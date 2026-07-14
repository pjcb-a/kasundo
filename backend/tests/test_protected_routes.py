from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_me_without_token_fails():
    response = client.get("/auth/me")
    assert response.status_code in [401, 403]


def test_get_debts_without_token_fails():
    response = client.get("/debts")
    assert response.status_code in [401, 403]


def test_get_notifications_without_token_fails():
    response = client.get("/notifications")
    assert response.status_code in [401, 403]


def test_get_dashboard_without_token_fails():
    response = client.get("/dashboard/summary")
    assert response.status_code in [401, 403]
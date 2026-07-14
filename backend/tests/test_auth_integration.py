def test_authenticated_user_can_get_profile(client, auth_headers):
    response = client.get(
        "/auth/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data
    assert "username" in data
    assert "email" in data


def test_authenticated_user_can_get_debts(client, auth_headers):
    response = client.get(
        "/debts",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_user_can_get_notifications(client, auth_headers):
    response = client.get(
        "/notifications",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_user_can_get_dashboard_summary(client, auth_headers):
    response = client.get(
        "/dashboard/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_borrowed_outstanding" in data
    assert "total_lent_outstanding" in data
    assert "unread_notifications_count" in data
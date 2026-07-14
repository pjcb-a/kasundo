import uuid


def create_and_accept_test_debt(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id,
    amount=300,
):
    """
    Helper function:
    1. Lender creates a debt request.
    2. Borrower accepts it.
    3. Returns the created debt object.
    """

    create_response = client.post(
        "/debt-requests",
        headers=lender_headers,
        json={
            "borrower_id": test_borrower_id,
            "amount": amount,
            "due_date": "2026-12-31",
            "purpose": f"Negative flow test {uuid.uuid4()}",
        },
    )

    assert create_response.status_code in [200, 201], create_response.text

    debt_request = create_response.json()
    request_id = debt_request["request_id"]

    accept_response = client.patch(
        f"/debt-requests/{request_id}/accept",
        headers=borrower_headers,
    )

    assert accept_response.status_code == 200, accept_response.text

    return accept_response.json()


def test_lender_cannot_record_payment(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.post(
        f"/payments/debt/{debt_id}",
        headers=lender_headers,
        json={
            "amount_paid": 100,
            "payment_method": "GCash",
            "notes": "Lender should not be able to pay",
        },
    )

    assert response.status_code == 403, response.text


def test_borrower_cannot_overpay(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.post(
        f"/payments/debt/{debt_id}",
        headers=borrower_headers,
        json={
            "amount_paid": 999,
            "payment_method": "GCash",
            "notes": "Overpayment should fail",
        },
    )

    assert response.status_code == 400, response.text


def test_borrower_cannot_manually_settle_debt(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.patch(
        f"/debts/{debt_id}/settle",
        headers=borrower_headers,
    )

    assert response.status_code == 403, response.text


def test_lender_cannot_settle_already_settled_debt(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    first_response = client.patch(
        f"/debts/{debt_id}/settle",
        headers=lender_headers,
    )

    assert first_response.status_code == 200, first_response.text

    second_response = client.patch(
        f"/debts/{debt_id}/settle",
        headers=lender_headers,
    )

    assert second_response.status_code == 400, second_response.text


def test_unrelated_user_cannot_accept_someone_elses_request(
    client,
    lender_headers,
    unrelated_headers,
    test_borrower_id,
):
    create_response = client.post(
        "/debt-requests",
        headers=lender_headers,
        json={
            "borrower_id": test_borrower_id,
            "amount": 300,
            "due_date": "2026-12-31",
            "purpose": f"Wrong borrower accept test {uuid.uuid4()}",
        },
    )

    assert create_response.status_code in [200, 201], create_response.text

    request_id = create_response.json()["request_id"]

    response = client.patch(
        f"/debt-requests/{request_id}/accept",
        headers=unrelated_headers,
    )

    assert response.status_code == 403, response.text


def test_unrelated_user_cannot_view_debt(
    client,
    lender_headers,
    borrower_headers,
    unrelated_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.get(
        f"/debts/{debt_id}",
        headers=unrelated_headers,
    )

    assert response.status_code == 403, response.text


def test_unrelated_user_cannot_view_payment_history(
    client,
    lender_headers,
    borrower_headers,
    unrelated_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.get(
        f"/payments/debt/{debt_id}",
        headers=unrelated_headers,
    )

    assert response.status_code == 403, response.text


def test_unrelated_user_cannot_view_debt_activity_logs(
    client,
    lender_headers,
    borrower_headers,
    unrelated_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.get(
        f"/activity-logs/debt/{debt_id}",
        headers=unrelated_headers,
    )

    assert response.status_code == 403, response.text


def test_unrelated_user_cannot_manually_settle_debt(
    client,
    lender_headers,
    borrower_headers,
    unrelated_headers,
    test_borrower_id,
):
    debt = create_and_accept_test_debt(
        client=client,
        lender_headers=lender_headers,
        borrower_headers=borrower_headers,
        test_borrower_id=test_borrower_id,
        amount=300,
    )

    debt_id = debt["debt_id"]

    response = client.patch(
        f"/debts/{debt_id}/settle",
        headers=unrelated_headers,
    )

    assert response.status_code == 403, response.text
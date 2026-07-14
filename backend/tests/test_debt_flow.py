def test_full_debt_request_accept_payment_flow(
    client,
    lender_headers,
    borrower_headers,
    test_borrower_id
):
    amount = 300
    payment_amount = 100

    # 1. Lender creates debt request
    create_response = client.post(
        "/debt-requests",
        headers=lender_headers,
        json={
            "borrower_id": test_borrower_id,
            "amount": amount,
            "due_date": "2026-12-31",
            "purpose": "Pytest full debt flow test"
        },
    )

    assert create_response.status_code in [200, 201], create_response.text

    debt_request = create_response.json()
    request_id = debt_request["request_id"]

    assert debt_request["borrower_id"] == test_borrower_id
    assert float(debt_request["amount"]) == float(amount)

    # 2. Borrower accepts debt request
    accept_response = client.patch(
        f"/debt-requests/{request_id}/accept",
        headers=borrower_headers,
    )

    assert accept_response.status_code == 200, accept_response.text

    debt = accept_response.json()
    debt_id = debt["debt_id"]

    assert debt["borrower_id"] == test_borrower_id
    assert float(debt["remaining_balance"]) == float(amount)
    assert debt["status"] == "Active"

    # 3. Borrower records partial payment
    payment_response = client.post(
        f"/payments/debt/{debt_id}",
        headers=borrower_headers,
        json={
            "amount_paid": payment_amount,
            "payment_method": "GCash",
            "notes": "Pytest partial payment"
        },
    )

    assert payment_response.status_code in [200, 201], payment_response.text

    payment = payment_response.json()

    assert payment["debt_id"] == debt_id
    assert float(payment["amount_paid"]) == float(payment_amount)

    # 4. Verify remaining balance
    debt_response = client.get(
        f"/debts/{debt_id}",
        headers=borrower_headers,
    )

    assert debt_response.status_code == 200

    updated_debt = debt_response.json()

    assert float(updated_debt["remaining_balance"]) == float(amount - payment_amount)
    assert updated_debt["status"] == "Active"

    # 5. Verify payment history
    history_response = client.get(
        f"/payments/debt/{debt_id}",
        headers=borrower_headers,
    )

    assert history_response.status_code == 200

    payments = history_response.json()

    assert any(
        item["debt_id"] == debt_id
        and float(item["amount_paid"]) == float(payment_amount)
        for item in payments
    )

    # 6. Verify activity log
    logs_response = client.get(
        f"/activity-logs/debt/{debt_id}",
        headers=borrower_headers,
    )

    assert logs_response.status_code == 200

    logs = logs_response.json()

    assert any(
        item["debt_id"] == debt_id
        and item["action"] == "PaymentRecorded"
        for item in logs
    )
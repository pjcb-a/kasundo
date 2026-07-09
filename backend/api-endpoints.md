# Kasundo API Endpoints

## Overview

Kasundo is a debt-tracking API built with FastAPI, SQLAlchemy, and PostgreSQL.

**Local base URL**

```text
http://127.0.0.1:8000
```

**Interactive API documentation**

```text
http://127.0.0.1:8000/docs
```

All protected endpoints require a JWT access token.

```http
Authorization: Bearer <access_token>
```

Dates and timestamps use ISO 8601 format. Stored timestamps should be treated as UTC.

---

# 1. Authentication

## Register User

```http
POST /auth/register
```

Authentication required: **No**

### Request body

```json
{
  "username": "juan_dela_cruz",
  "email": "juan@example.com",
  "phone_number": "09171234567",
  "password": "secure-password"
}
```

### Success response

```text
200 OK
```

```json
{
  "user_id": 1,
  "username": "juan_dela_cruz",
  "email": "juan@example.com",
  "phone_number": "09171234567",
  "created_at": "2026-07-06T10:00:00Z"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `400` | Username, email, or phone number is already registered |
| `422` | Invalid or missing request fields |

---

## Login

```http
POST /auth/login
```

Authentication required: **No**

The `login` field may contain a username, email address, or phone number.

### Request body

```json
{
  "login": "juan_dela_cruz",
  "password": "secure-password"
}
```

### Success response

```text
200 OK
```

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `401` | Incorrect login credentials |
| `422` | Invalid request body |

---

## Get Current User

```http
GET /auth/me
```

Authentication required: **Yes**

### Success response

```text
200 OK
```

```json
{
  "user_id": 1,
  "username": "juan_dela_cruz",
  "email": "juan@example.com",
  "phone_number": "09171234567",
  "created_at": "2026-07-06T10:00:00Z"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `401` | Missing, invalid, or expired JWT |

---

# 2. Debt Requests

## Create Debt Request

```http
POST /debt-requests
```

Authentication required: **Yes**

The authenticated user becomes the lender.

### Request body

```json
{
  "borrower_id": 2,
  "amount": 500.0,
  "due_date": "2026-12-31",
  "message": "Payment for shared project expenses"
}
```

### Success response

```text
201 Created
```

```json
{
  "request_id": 15,
  "lender_id": 1,
  "borrower_id": 2,
  "amount": 500.0,
  "due_date": "2026-12-31",
  "status": "Pending",
  "message": "Payment for shared project expenses",
  "created_at": "2026-07-06T10:00:00Z"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `400` | Invalid request or lender attempted to select themselves |
| `404` | Borrower does not exist |
| `401` | Authentication required |
| `422` | Invalid amount, date, or request fields |

---

## Get Sent Debt Requests

```http
GET /debt-requests/sent
```

Authentication required: **Yes**

Returns requests created by the authenticated user.

### Success response

```text
200 OK
```

```json
[
  {
    "request_id": 15,
    "lender_id": 1,
    "borrower_id": 2,
    "amount": 500.0,
    "due_date": "2026-12-31",
    "status": "Pending",
    "message": "Payment for shared project expenses",
    "created_at": "2026-07-06T10:00:00Z"
  }
]
```

---

## Get Received Debt Requests

```http
GET /debt-requests/received
```

Authentication required: **Yes**

Returns requests where the authenticated user is the borrower.

### Success response

```text
200 OK
```

```json
[
  {
    "request_id": 15,
    "lender_id": 1,
    "borrower_id": 2,
    "amount": 500.0,
    "due_date": "2026-12-31",
    "status": "Pending",
    "message": "Payment for shared project expenses",
    "created_at": "2026-07-06T10:00:00Z"
  }
]
```

---

## Accept Debt Request

```http
PATCH /debt-requests/{request_id}/accept
```

Authentication required: **Yes**

Only the borrower assigned to the request may accept it.

No request body is required.

### Success response

```text
200 OK
```

Accepting a request creates a new debt.

```json
{
  "debt_id": 8,
  "request_id": 15,
  "lender_id": 1,
  "borrower_id": 2,
  "original_amount": 500.0,
  "remaining_balance": 500.0,
  "due_date": "2026-12-31",
  "status": "Active",
  "created_at": "2026-07-06T10:00:00Z",
  "updated_at": "2026-07-06T10:00:00Z",
  "settled_at": null
}
```

### Common errors

| Status | Meaning |
|---|---|
| `400` | Request has already been processed |
| `403` | Current user is not the assigned borrower |
| `404` | Debt request not found |
| `401` | Authentication required |

---

## Reject Debt Request

```http
PATCH /debt-requests/{request_id}/reject
```

Authentication required: **Yes**

Only the assigned borrower may reject the request.

No request body is required.

### Success response

```text
200 OK
```

```json
{
  "request_id": 15,
  "lender_id": 1,
  "borrower_id": 2,
  "amount": 500.0,
  "due_date": "2026-12-31",
  "status": "Rejected",
  "message": "Payment for shared project expenses",
  "created_at": "2026-07-06T10:00:00Z"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `400` | Request has already been processed |
| `403` | Current user is not the assigned borrower |
| `404` | Debt request not found |
| `401` | Authentication required |

---

# 3. Debts

## Get User Debts

```http
GET /debts
```

Authentication required: **Yes**

Returns debts where the current user is the lender or borrower.

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `role` | string | No | `lender` or `borrower` |
| `status` | string | No | `Active`, `Settled`, or `Overdue` |
| `limit` | integer | No | Number of records, default `10`, range `1–50` |
| `offset` | integer | No | Number of records to skip, default `0` |

### Examples

```http
GET /debts?role=borrower
GET /debts?role=lender
GET /debts?status=Active
GET /debts?role=borrower&status=Settled
GET /debts?limit=5&offset=0
```

### Success response

```text
200 OK
```

```json
[
  {
    "debt_id": 8,
    "request_id": 15,
    "lender_id": 1,
    "borrower_id": 2,
    "original_amount": 500.0,
    "remaining_balance": 500.0,
    "due_date": "2026-12-31",
    "status": "Active",
    "created_at": "2026-07-06T10:00:00Z",
    "updated_at": "2026-07-06T10:00:00Z",
    "settled_at": null
  }
]
```

### Common errors

| Status | Meaning |
|---|---|
| `401` | Authentication required |
| `422` | Invalid role, status, limit, or offset |

---

## Get Debt by ID

```http
GET /debts/{debt_id}
```

Authentication required: **Yes**

Only the lender or borrower may view the debt.

### Success response

```text
200 OK
```

```json
{
  "debt_id": 8,
  "request_id": 15,
  "lender_id": 1,
  "borrower_id": 2,
  "original_amount": 500.0,
  "remaining_balance": 500.0,
  "due_date": "2026-12-31",
  "status": "Active",
  "created_at": "2026-07-06T10:00:00Z",
  "updated_at": "2026-07-06T10:00:00Z",
  "settled_at": null
}
```

### Common errors

| Status | Meaning |
|---|---|
| `403` | Current user is not part of the debt |
| `404` | Debt not found |
| `401` | Authentication required |

---

## Manually Settle Debt

```http
PATCH /debts/{debt_id}/settle
```

Authentication required: **Yes**

Only the lender may manually confirm settlement.

This endpoint may represent a payment made outside Kasundo, such as cash or a direct bank transfer.

No request body is required.

### Success response

```text
200 OK
```

```json
{
  "debt_id": 8,
  "request_id": 15,
  "lender_id": 1,
  "borrower_id": 2,
  "original_amount": 500.0,
  "remaining_balance": 0.0,
  "due_date": "2026-12-31",
  "status": "Settled",
  "created_at": "2026-07-06T10:00:00Z",
  "updated_at": "2026-07-06T10:20:00Z",
  "settled_at": "2026-07-06T10:20:00Z"
}
```

### Side effects

- Updates the debt status to `Settled`
- Sets the remaining balance to `0`
- Creates a `DebtSettled` activity log
- Sends a settlement notification to the borrower

### Common errors

| Status | Meaning |
|---|---|
| `400` | Debt is already settled |
| `403` | Current user is not the lender |
| `404` | Debt not found |
| `401` | Authentication required |

---

# 4. Payments

## Record Payment

```http
POST /payments/debt/{debt_id}
```

Authentication required: **Yes**

Only the borrower may record a payment.

### Request body

```json
{
  "amount_paid": 200.0,
  "payment_method": "GCash",
  "notes": "Partial payment"
}
```

### Success response

```text
200 OK
```

```json
{
  "payment_id": 8,
  "debt_id": 7,
  "created_by": 2,
  "amount_paid": "200.00",
  "payment_method": "GCash",
  "notes": "Partial payment",
  "paid_at": "2026-07-06T10:00:00Z"
}
```

### Business rules

- Payment amount must be greater than zero
- Payment amount cannot exceed the remaining balance
- A settled debt cannot receive another payment
- When the remaining balance reaches zero, the debt is automatically settled
- Payment creation, balance update, notifications, and activity logs are committed as one transaction
- The debt row is locked while a payment is being processed to prevent concurrent overpayment

### Common errors

| Status | Meaning |
|---|---|
| `400` | Invalid amount, overpayment, or debt already settled |
| `403` | Current user is not the borrower |
| `404` | Debt not found |
| `401` | Authentication required |
| `422` | Invalid request body |

---

## Get Payment History

```http
GET /payments/debt/{debt_id}
```

Authentication required: **Yes**

Only the lender or borrower may view the payment history.

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Default `10`, range `1–50` |
| `offset` | integer | No | Default `0` |

### Examples

```http
GET /payments/debt/7?limit=5&offset=0
GET /payments/debt/7?limit=5&offset=5
```

### Success response

```text
200 OK
```

```json
[
  {
    "payment_id": 8,
    "debt_id": 7,
    "created_by": 2,
    "amount_paid": "200.00",
    "payment_method": "GCash",
    "notes": "Partial payment",
    "paid_at": "2026-07-06T10:00:00Z"
  }
]
```

### Common errors

| Status | Meaning |
|---|---|
| `403` | Current user is not part of the debt |
| `404` | Debt not found |
| `401` | Authentication required |
| `422` | Invalid limit or offset |

---

# 5. Notifications

## Get Notifications

```http
GET /notifications
```

Authentication required: **Yes**

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Default `10`, range `1–50` |
| `offset` | integer | No | Default `0` |
| `is_read` | boolean | No | Filter by read state |

### Examples

```http
GET /notifications?limit=5&offset=0
GET /notifications?is_read=false
GET /notifications?is_read=true
```

### Success response

```text
200 OK
```

```json
[
  {
    "notification_id": 26,
    "user_id": 2,
    "title": "Debt Settled",
    "message": "The lender manually confirmed that this debt has been settled.",
    "type": "DebtSettled",
    "is_read": false,
    "created_at": "2026-07-06T10:20:00Z"
  }
]
```

### Notification types

```text
DebtRequest
DebtAccepted
DebtRejected
Reminder
Overdue
PaymentRecorded
DebtSettled
```

---

## Mark Notification as Read

```http
PATCH /notifications/{notification_id}/read
```

Authentication required: **Yes**

Only the owner of the notification may update it.

No request body is required.

### Success response

```text
200 OK
```

```json
{
  "notification_id": 26,
  "user_id": 2,
  "title": "Debt Settled",
  "message": "The lender manually confirmed that this debt has been settled.",
  "type": "DebtSettled",
  "is_read": true,
  "created_at": "2026-07-06T10:20:00Z"
}
```

### Common errors

| Status | Meaning |
|---|---|
| `403` | Current user does not own the notification |
| `404` | Notification not found |
| `401` | Authentication required |

---

## Mark All Notifications as Read

```http
PATCH /notifications/read-all
```

Authentication required: **Yes**

No request body is required.

### Success response

```text
200 OK
```

Returns the notifications that were updated.

```json
[
  {
    "notification_id": 26,
    "user_id": 2,
    "title": "Debt Settled",
    "message": "The lender manually confirmed that this debt has been settled.",
    "type": "DebtSettled",
    "is_read": true,
    "created_at": "2026-07-06T10:20:00Z"
  }
]
```

---

## Get Unread Notification Count

```http
GET /notifications/unread-count
```

Authentication required: **Yes**

### Success response

```text
200 OK
```

```json
{
  "unread_count": 8
}
```

---

# 6. Activity Logs

## Get My Activity Logs

```http
GET /activity-logs
```

Authentication required: **Yes**

Returns activity performed by the authenticated user.

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Default `10`, range `1–50` |
| `offset` | integer | No | Default `0` |
| `action` | string | No | Filter by activity action |

### Examples

```http
GET /activity-logs?limit=5&offset=0
GET /activity-logs?action=PaymentRecorded
```

### Success response

```text
200 OK
```

```json
[
  {
    "log_id": 13,
    "debt_id": 8,
    "actor_id": 1,
    "action": "DebtSettled",
    "details": "Lender 1 manually confirmed Debt 8 was fully settled.",
    "created_at": "2026-07-06T10:20:00Z"
  }
]
```

### Activity actions

```text
DebtRequestCreated
DebtRequestAccepted
DebtRequestRejected
PaymentRecorded
DebtSettled
NotificationRead
AllNotificationsRead
```

---

## Get Activity Logs for a Debt

```http
GET /activity-logs/debt/{debt_id}
```

Authentication required: **Yes**

Only the lender or borrower may view the debt activity.

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Default `10`, range `1–50` |
| `offset` | integer | No | Default `0` |
| `action` | string | No | Filter by activity action |

### Example

```http
GET /activity-logs/debt/8?action=DebtSettled
```

### Success response

```text
200 OK
```

```json
[
  {
    "log_id": 13,
    "debt_id": 8,
    "actor_id": 1,
    "action": "DebtSettled",
    "details": "Lender 1 manually confirmed Debt 8 was fully settled.",
    "created_at": "2026-07-06T10:20:00Z"
  }
]
```

### Common errors

| Status | Meaning |
|---|---|
| `403` | Current user is not part of the debt |
| `404` | Debt not found |
| `401` | Authentication required |
| `422` | Invalid query parameter |

---

# 7. Dashboard

## Get Dashboard Summary

```http
GET /dashboard/summary
```

Authentication required: **Yes**

### Success response

```text
200 OK
```

```json
{
  "total_borrowed_outstanding": 2000.0,
  "total_lent_outstanding": 0.0,
  "total_payments_made": 2372.0,
  "total_payments_received": 0.0,
  "active_borrowed_count": 3,
  "active_lent_count": 0,
  "settled_borrowed_count": 4,
  "settled_lent_count": 0,
  "pending_received_requests": 3,
  "pending_sent_requests": 1,
  "unread_notifications_count": 8
}
```

---

## Get Recent Payments

```http
GET /dashboard/recent-payments
```

Authentication required: **Yes**

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Maximum number of recent payments |

### Example

```http
GET /dashboard/recent-payments?limit=5
```

### Success response

```text
200 OK
```

```json
[
  {
    "payment_id": 8,
    "debt_id": 7,
    "created_by": 2,
    "amount_paid": "200.00",
    "payment_method": "GCash",
    "notes": "Partial payment",
    "paid_at": "2026-07-06T10:00:00Z"
  }
]
```

---

## Get Recent Activity

```http
GET /dashboard/recent-activity
```

Authentication required: **Yes**

This endpoint returns activity related to the current user, including activity performed by the other party on a debt involving the current user.

### Query parameters

| Parameter | Type | Required | Description |
|---|---:|---:|---|
| `limit` | integer | No | Maximum number of activity records |

### Example

```http
GET /dashboard/recent-activity?limit=10
```

### Success response

```text
200 OK
```

```json
[
  {
    "log_id": 7,
    "debt_id": 7,
    "actor_id": 2,
    "action": "PaymentRecorded",
    "details": "User 2 recorded a payment of 200 for Debt 7.",
    "created_at": "2026-07-06T10:00:00Z"
  }
]
```

---

# 8. Standard Error Responses

## Unauthorized

```text
401 Unauthorized
```

```json
{
  "detail": "Could not validate credentials"
}
```

## Forbidden

```text
403 Forbidden
```

```json
{
  "detail": "You are not allowed to access this resource."
}
```

## Not Found

```text
404 Not Found
```

```json
{
  "detail": "Resource not found."
}
```

## Business Rule Violation

```text
400 Bad Request
```

```json
{
  "detail": "Debt is already settled."
}
```

## Validation Error

```text
422 Unprocessable Content
```

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": [
        "query",
        "limit"
      ],
      "msg": "Input should be greater than or equal to 1",
      "input": "0"
    }
  ]
}
```

---

# 9. Frontend Integration Notes

1. Store the JWT securely and send it in the `Authorization` header.
2. Treat `401` responses as an expired or invalid session.
3. Use `403` to show that the authenticated user does not have permission.
4. Use `422` responses to display field-level validation messages.
5. Use `limit` and `offset` for paginated lists.
6. Refresh the dashboard after payments, settlements, or debt-request updates.
7. Refresh the unread notification count after marking notifications as read.
8. Money values should be displayed using two decimal places.
9. Timestamps returned by the API should be converted to the user's local timezone in the frontend.
10. A manually settled debt is lender-confirmed and may represent an external payment.

---

# 10. Recommended Mobile App Flow

```text
Login
  → Dashboard
  → View sent/received debt requests
  → Accept or reject request
  → View active debts
  → Record payment as borrower
  → Confirm manual settlement as lender
  → View payment history
  → View notifications
  → View activity history
```

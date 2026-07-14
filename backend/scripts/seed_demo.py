import sys
from pathlib import Path
from datetime import date, datetime, UTC
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.database import SessionLocal
from app.models.user import User
from app.models.debt_request import DebtRequest
from app.models.debt import Debt
from app.models.payment import Payment

from app.enums import (
    DebtRequestStatus,
    DebtStatus,
    ActivityAction,
    NotificationType,
)

from app.services.activity_log_service import create_activity_log
from app.services.notification_service import create_notification

try:
    from app.security import get_password_hash
except ImportError:
    from app.security import hash_password as get_password_hash


DEMO_PASSWORD = "password123"


def get_or_create_user(
    db,
    username: str,
    email: str,
    phone_number: str,
    first_name: str,
    last_name: str,
) -> User:
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user:
        print(f"User already exists: {username}")
        return user

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        phone_number=phone_number,
        password_hash=get_password_hash(DEMO_PASSWORD),
    )

    db.add(user)
    db.flush()

    print(f"Created user: {username}")

    return user


def create_pending_request_if_missing(
    db,
    lender: User,
    borrower: User,
) -> DebtRequest:
    existing_request = (
        db.query(DebtRequest)
        .filter(DebtRequest.purpose == "Seed Demo - Pending Request")
        .first()
    )

    if existing_request:
        print("Pending request already exists.")
        return existing_request

    debt_request = DebtRequest(
        lender_id=lender.user_id,
        borrower_id=borrower.user_id,
        amount=Decimal("1500.00"),
        due_date=date(2026, 12, 31),
        purpose="Seed Demo - Pending Request",
        status=DebtRequestStatus.PENDING,
    )

    db.add(debt_request)
    db.flush()

    create_activity_log(
        db=db,
        actor_id=lender.user_id,
        debt_id=None,
        action=ActivityAction.DEBT_REQUEST_CREATED,
        details=(
            f"Demo lender {lender.user_id} created a pending debt "
            f"request for borrower {borrower.user_id}."
        ),
    )

    create_notification(
        db=db,
        user_id=borrower.user_id,
        notification_type=NotificationType.DEBT_REQUEST,
        title="New Demo Debt Request",
        message="You received a demo debt request.",
    )

    print("Created pending debt request.")

    return debt_request


def create_active_debt_if_missing(
    db,
    lender: User,
    borrower: User,
) -> Debt:
    existing_debt = (
        db.query(Debt)
        .filter(Debt.purpose == "Seed Demo - Active Debt")
        .first()
    )

    if existing_debt:
        print("Active demo debt already exists.")
        return existing_debt

    accepted_request = DebtRequest(
        lender_id=lender.user_id,
        borrower_id=borrower.user_id,
        amount=Decimal("1000.00"),
        due_date=date(2026, 12, 31),
        purpose="Seed Demo - Active Debt",
        status=DebtRequestStatus.ACCEPTED,
    )

    db.add(accepted_request)
    db.flush()

    debt = Debt(
        request_id=accepted_request.request_id,
        lender_id=lender.user_id,
        borrower_id=borrower.user_id,
        original_amount=Decimal("1000.00"),
        remaining_balance=Decimal("700.00"),
        due_date=date(2026, 12, 31),
        purpose="Seed Demo - Active Debt",
        status=DebtStatus.ACTIVE,
    )

    db.add(debt)
    db.flush()

    payment = Payment(
        debt_id=debt.debt_id,
        created_by=borrower.user_id,
        amount_paid=Decimal("300.00"),
        payment_method="GCash",
        notes="Seed demo partial payment",
        paid_at=datetime.now(UTC),
    )

    db.add(payment)
    db.flush()

    create_activity_log(
        db=db,
        actor_id=borrower.user_id,
        debt_id=debt.debt_id,
        action=ActivityAction.PAYMENT_RECORDED,
        details=(
            f"Demo borrower {borrower.user_id} recorded a payment "
            f"of 300 for Debt {debt.debt_id}."
        ),
    )

    create_notification(
        db=db,
        user_id=lender.user_id,
        notification_type=NotificationType.PAYMENT_RECORDED,
        title="Demo Payment Recorded",
        message="A demo borrower recorded a payment.",
    )

    print("Created active demo debt with partial payment.")

    return debt


def create_settled_debt_if_missing(
    db,
    lender: User,
    borrower: User,
) -> Debt:
    existing_debt = (
        db.query(Debt)
        .filter(Debt.purpose == "Seed Demo - Settled Debt")
        .first()
    )

    if existing_debt:
        print("Settled demo debt already exists.")
        return existing_debt

    accepted_request = DebtRequest(
        lender_id=lender.user_id,
        borrower_id=borrower.user_id,
        amount=Decimal("500.00"),
        due_date=date(2026, 10, 31),
        purpose="Seed Demo - Settled Debt",
        status=DebtRequestStatus.ACCEPTED,
    )

    db.add(accepted_request)
    db.flush()

    debt = Debt(
        request_id=accepted_request.request_id,
        lender_id=lender.user_id,
        borrower_id=borrower.user_id,
        original_amount=Decimal("500.00"),
        remaining_balance=Decimal("0.00"),
        due_date=date(2026, 10, 31),
        purpose="Seed Demo - Settled Debt",
        status=DebtStatus.SETTLED,
        settled_at=datetime.now(UTC),
    )

    db.add(debt)
    db.flush()

    payment = Payment(
        debt_id=debt.debt_id,
        created_by=borrower.user_id,
        amount_paid=Decimal("500.00"),
        payment_method="Bank Transfer",
        notes="Seed demo full payment",
        paid_at=datetime.now(UTC),
    )

    db.add(payment)
    db.flush()

    create_activity_log(
        db=db,
        actor_id=borrower.user_id,
        debt_id=debt.debt_id,
        action=ActivityAction.PAYMENT_RECORDED,
        details=(
            f"Demo borrower {borrower.user_id} recorded a full payment "
            f"for Debt {debt.debt_id}."
        ),
    )

    create_activity_log(
        db=db,
        actor_id=borrower.user_id,
        debt_id=debt.debt_id,
        action=ActivityAction.DEBT_SETTLED,
        details=f"Demo Debt {debt.debt_id} was settled.",
    )

    create_notification(
        db=db,
        user_id=lender.user_id,
        notification_type=NotificationType.DEBT_SETTLED,
        title="Demo Debt Settled",
        message="A demo debt has been fully settled.",
    )

    create_notification(
        db=db,
        user_id=borrower.user_id,
        notification_type=NotificationType.DEBT_SETTLED,
        title="Demo Debt Settled",
        message="Your demo debt has been fully settled.",
    )

    print("Created settled demo debt with full payment.")

    return debt


def main():
    db = SessionLocal()

    try:
        lender = get_or_create_user(
            db=db,
            username="demo_lender",
            email="demo_lender@example.com",
            phone_number="09000000001",
            first_name="Demo",
            last_name="Lender",
        )

        borrower = get_or_create_user(
            db=db,
            username="demo_borrower",
            email="demo_borrower@example.com",
            phone_number="09000000002",
            first_name="Demo",
            last_name="Borrower",
        )

        unrelated = get_or_create_user(
            db=db,
            username="demo_unrelated",
            email="demo_unrelated@example.com",
            phone_number="09000000003",
            first_name="Demo",
            last_name="Unrelated",
        )

        create_pending_request_if_missing(
            db=db,
            lender=lender,
            borrower=borrower,
        )

        create_active_debt_if_missing(
            db=db,
            lender=lender,
            borrower=borrower,
        )

        create_settled_debt_if_missing(
            db=db,
            lender=lender,
            borrower=borrower,
        )

        db.commit()

        print("\nSeed demo data completed successfully.")
        print("\nDemo accounts:")
        print("demo_lender / password123")
        print("demo_borrower / password123")
        print("demo_unrelated / password123")

        print(f"\nDemo unrelated user ID: {unrelated.user_id}")

    except Exception as error:
        db.rollback()
        print("\nSeed failed. Rolled back changes.")
        print(error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
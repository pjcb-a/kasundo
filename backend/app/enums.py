from enum import Enum


class DebtRequestStatus(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"


class DebtStatus(str, Enum):
    ACTIVE = "Active"
    SETTLED = "Settled"
    OVERDUE = "Overdue"


class NotificationType(str, Enum):
    DEBT_REQUEST = "DebtRequest"
    DEBT_ACCEPTED = "DebtAccepted"
    DEBT_REJECTED = "DebtRejected"
    REMINDER = "Reminder"
    OVERDUE = "Overdue"
    PAYMENT_RECORDED = "PaymentRecorded"
    DEBT_SETTLED = "DebtSettled"
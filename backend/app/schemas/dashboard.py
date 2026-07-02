from pydantic import BaseModel

class DashboardSummaryResponse(BaseModel):
    total_borrowed_outstanding: float
    total_lent_outstanding: float

    total_payments_made: float
    total_payments_received: float

    active_borrowed_count: int 
    active_lent_count: int 

    settled_borrowed_count: int
    settled_lent_count: int

    pending_received_requests: int
    pending_sent_requests: int 

    unread_notifications_count: int
    
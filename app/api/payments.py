from fastapi import APIRouter

from app.database import get_payment_events

router = APIRouter()


@router.get("/api/payments")
def get_payments():
    rows = get_payment_events()

    return [
        {
            "event_id": row[0],
            "payment_id": row[1],
            "status": row[2],
            "failure_reason": row[3],
            "amount": row[4],
            "customer_name": row[5],
            "customer_email": row[6],
            "received_at": row[7],
        }
        for row in rows
    ]
from fastapi import APIRouter, Header, HTTPException

from app.models.payment_event import PaymentEvent
from app.services.webhook import handle_payment_event
from app.database import payment_event_exists


router = APIRouter()


@router.post("/webhooks/payment")
def payment_webhook(
    event: PaymentEvent,
    x_webhook_signature: str = Header(...)
):
    if x_webhook_signature != "mock-signature":
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )

    if payment_event_exists(event.event_id):
        return {
            "status": "already_processed",
            "event_id": event.event_id
        }

    customer_message = event.customer_message if hasattr(event, "customer_message") else ""

    return handle_payment_event(
        event=event,
        customer_message=customer_message
    )
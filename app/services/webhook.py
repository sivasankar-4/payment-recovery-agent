from app.database import save_payment_event
from app.services.recovery import recover_payment
from app.services.systemic_detector import detect_systemic_failure


def handle_payment_event(event: dict, customer_message: str):

    save_payment_event(event)
    # Get payment information from the webhook event
    payment_id = event.payment_id
    event_id = event.event_id

    # Temporary values — we'll replace these with real logic
    systemic = detect_systemic_failure()
    retry_count = 0
    recovery_score = 95

    result = recover_payment(
        message=customer_message,
        systemic=systemic,
        retry_count=retry_count,
        recovery_score=recovery_score,
        event_id=event_id,
        payment_id=payment_id,
    )

    return result
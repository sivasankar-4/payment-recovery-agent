from app.services.webhook import handle_payment_event


event = {
    "payment_id": "pay_123",
    "status": "failed",
}

result = handle_payment_event(
    event=event,
    customer_message="I can pay next Monday.",
)

print("Webhook result:")
print(result)
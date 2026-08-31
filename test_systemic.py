import requests
from uuid import uuid4

WEBHOOK_URL = "http://127.0.0.1:8000/webhooks/payment"

events = [
    ("evt_sys_001", "pay_sys_001", "Siva", "siva@example.com"),
    ("evt_sys_002", "pay_sys_002", "Priya", "priya@example.com"),
    ("evt_sys_003", "pay_sys_003", "Arjun", "arjun@example.com"),
    ("evt_sys_004", "pay_sys_004", "Kiran", "kiran@example.com"),
    ("evt_sys_005", "pay_sys_005", "Neha", "neha@example.com"),
]

for event_id, payment_id, name, email in events:
    event_id = f"{event_id}_{uuid4().hex}"
    data = {
        "event_id": event_id,
        "payment_id": payment_id,
        "status": "failed",
        "failure_reason": "INSUFFICIENT_FUNDS",
        "amount": 2000,
        "customer": {
            "name": name,
            "email": email
        }
    }

    response = requests.post(WEBHOOK_URL, json=data)

    print(event_id, response.status_code)

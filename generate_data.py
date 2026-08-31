import requests

WEBHOOK_URL = "http://127.0.0.1:8000/webhooks/payment"

normal_events = [
    {
        "event_id": "evt_normal_001",
        "payment_id": "pay_normal_001",
        "status": "failed",
        "failure_reason": "INSUFFICIENT_FUNDS",
        "amount": 2000,
        "customer": {
            "name": "Siva",
            "email": "siva@example.com"
        }
    },
    {
        "event_id": "evt_normal_002",
        "payment_id": "pay_normal_002",
        "status": "success",
        "failure_reason": "NONE",
        "amount": 1500,
        "customer": {
            "name": "Priya",
            "email": "priya@example.com"
        }
    },
    {
        "event_id": "evt_normal_003",
        "payment_id": "pay_normal_003",
        "status": "success",
        "failure_reason": "NONE",
        "amount": 3000,
        "customer": {
            "name": "Arjun",
            "email": "arjun@example.com"
        }
    },
    {
        "event_id": "evt_normal_004",
        "payment_id": "pay_normal_004",
        "status": "failed",
        "failure_reason": "CARD_EXPIRED",
        "amount": 2500,
        "customer": {
            "name": "Kiran",
            "email": "kiran@example.com"
        }
    },
    {
        "event_id": "evt_normal_005",
        "payment_id": "pay_normal_005",
        "status": "success",
        "failure_reason": "NONE",
        "amount": 1800,
        "customer": {
            "name": "Neha",
            "email": "neha@example.com"
        }
    }
]

customer_failure_events = [
    {
        "event_id": "evt_customer_001",
        "payment_id": "pay_customer_001",
        "status": "failed",
        "failure_reason": "INSUFFICIENT_FUNDS",
        "amount": 2000,
        "customer": {
            "name": "Siva",
            "email": "siva@example.com"
        }
    },
    {
        "event_id": "evt_customer_002",
        "payment_id": "pay_customer_002",
        "status": "failed",
        "failure_reason": "INSUFFICIENT_FUNDS",
        "amount": 2500,
        "customer": {
            "name": "Siva",
            "email": "siva@example.com"
        }
    },
    {
        "event_id": "evt_customer_003",
        "payment_id": "pay_customer_003",
        "status": "failed",
        "failure_reason": "INSUFFICIENT_FUNDS",
        "amount": 1800,
        "customer": {
            "name": "Siva",
            "email": "siva@example.com"
        }
    }
]

for event in normal_events:
    response = requests.post(WEBHOOK_URL, json=event)

    print("EVENT:", event["event_id"])
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


for event in customer_failure_events:
    response = requests.post(WEBHOOK_URL, json=event)

    print("EVENT:", event["event_id"])
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
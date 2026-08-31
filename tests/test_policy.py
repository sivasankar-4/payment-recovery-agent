from app.services.policy import evaluate_policy
from app.schemas.intent import Intent


tests = [
    {
        "name": "Systemic failure",
        "systemic": True,
        "retry_count": 0,
        "recovery_score": 95,
        "confidence": 0.95,
        "intent": Intent.READY_TO_PAY,
    },
    {
        "name": "Retry limit reached",
        "systemic": False,
        "retry_count": 2,
        "recovery_score": 95,
        "confidence": 0.95,
        "intent": Intent.READY_TO_PAY,
    },
    {
        "name": "Low confidence",
        "systemic": False,
        "retry_count": 0,
        "recovery_score": 95,
        "confidence": 0.55,
        "intent": Intent.READY_TO_PAY,
    },
    {
        "name": "Low recovery score",
        "systemic": False,
        "retry_count": 0,
        "recovery_score": 40,
        "confidence": 0.95,
        "intent": Intent.READY_TO_PAY,
    },
    {
        "name": "Ready to pay",
        "systemic": False,
        "retry_count": 0,
        "recovery_score": 95,
        "confidence": 0.95,
        "intent": Intent.READY_TO_PAY,
    },
    {
        "name": "Payment delay",
        "systemic": False,
        "retry_count": 0,
        "recovery_score": 95,
        "confidence": 0.95,
        "intent": Intent.PAYMENT_DELAY,
    },
]


for test in tests:
    result = evaluate_policy(
        systemic=test["systemic"],
        retry_count=test["retry_count"],
        recovery_score=test["recovery_score"],
        confidence=test["confidence"],
        intent=test["intent"],
    )

    print(f"{test['name']}: {result.action} -> {result.reason}")
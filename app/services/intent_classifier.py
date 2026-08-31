from app.schemas.intentresult import IntentResult
from app.schemas.intent import Intent


def classify_intent(message: str) -> IntentResult:

    message = message.lower()

    if "next monday" in message or "later" in message:
        return IntentResult(
            intent=Intent.PAYMENT_DELAY,
            confidence=0.95
        )

    if "pay now" in message or "ready to pay" in message:
        return IntentResult(
            intent=Intent.READY_TO_PAY,
            confidence=0.95
        )

    return IntentResult(
        intent=Intent.UNKNOWN,
        confidence=0.40
    )
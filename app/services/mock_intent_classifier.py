from app.schemas.intent import Intent
from app.schemas.intentresult import IntentResult


def classify_intent(message: str) -> IntentResult:
    normalized_message = message.lower()

    payment_delay_signals = [
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "next week",
        "tomorrow",
    ]

    if any(signal in normalized_message for signal in payment_delay_signals):
        return IntentResult(
            intent=Intent.PAYMENT_DELAY,
            confidence=0.95
        )

    if any(
        signal in normalized_message
        for signal in ("don't want to pay", "do not want to pay", "decline", "declined")
    ):
        return IntentResult(
            intent=Intent.DECLINED,
            confidence=0.9
        )

    if any(
        signal in normalized_message
        for signal in ("add money", "ready to pay", "pay now")
    ):
        return IntentResult(
            intent=Intent.READY_TO_PAY,
            confidence=0.9
        )

    if (
        (
            "card" in normalized_message
            and any(
                signal in normalized_message
                for signal in ("new", "update", "replace", "change", "expired")
            )
        )
        or "payment method" in normalized_message
    ):
        return IntentResult(
            intent=Intent.UPDATE_PAYMENT_METHOD,
            confidence=0.9
        )

    if any(
        signal in normalized_message
        for signal in ("why did", "failed", "failure", "what happened")
    ):
        return IntentResult(
            intent=Intent.PAYMENT_FAILURE_QUERY,
            confidence=0.8
        )

    return IntentResult(
        intent=Intent.UNKNOWN,
        confidence=0.3
    )
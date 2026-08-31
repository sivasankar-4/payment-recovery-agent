from app.services.mock_intent_classifier import classify_intent


messages = [
    "I can pay next Wednesday.",
    "I'll add money and pay now.",
    "My card expired.",
    "Why did my payment fail?",
    "I don't want to pay anymore.",
    "Something strange happened.",
]

for message in messages:
    result = classify_intent(message)

    print(f"Message: {message}")
    print(f"Intent: {result.intent}")
    print(f"Confidence: {result.confidence}")
    print("-" * 40)
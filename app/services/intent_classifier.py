from openai import OpenAI
from app.schemas.intentresult import IntentResult


client = OpenAI()


def classify_intent(message: str) -> IntentResult:
    response = client.responses.parse(
        model="gpt-5.5",
        input=[
            {
                "role": "system",
                "content": """
                Classify the customer's payment message into exactly one
                of the available intents.

                Available intents:
                - READY_TO_PAY
                - PAYMENT_DELAY
                - UPDATE_PAYMENT_METHOD
                - PAYMENT_FAILURE_QUERY
                - DECLINED
                - UNKNOWN

                Return a confidence score between 0.0 and 1.0.
                Do not decide or execute any recovery action.
                Only classify the customer's intent.
                """
            },
            {
                "role": "user",
                "content": message
            }
        ],
        text_format=IntentResult,
    )

    return response.output_parsed
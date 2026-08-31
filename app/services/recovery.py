from app.services.policy import evaluate_policy
from app.services.action_executor import execute_action
from app.services.intent_classifier import classify_intent
from app.database import save_audit_log


def recover_payment(
    message: str,
    systemic: bool,
    retry_count: int,
    recovery_score: float,
    event_id: str,
    payment_id: str,
):
    #classify the intent of the message
    intent_result = classify_intent(message)

    #evaluate the policy based on the intent, confidence, recovery score, systemic flag, and retry count
    policy_result = evaluate_policy(
        systemic=systemic,
        retry_count=retry_count,
        recovery_score=recovery_score,
        confidence=intent_result.confidence,
        intent=intent_result.intent,
    )

    save_audit_log(
        event_id=event_id,
        payment_id=payment_id,
        intent=intent_result.intent.value,
        confidence=intent_result.confidence,
        recovery_score=recovery_score,
        systemic=systemic,
        retry_count=retry_count,
        action=policy_result.action.value,
        reason=policy_result.reason,
    )
   
    #execute the action based on the policy result
    result = execute_action(policy_result)

    return result
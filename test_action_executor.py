from app.services.action_executor import execute_action
from app.schemas.action import Action
from app.schemas.policyresult import PolicyResult



result = PolicyResult(
    action=Action.SEND_PAYMENT_LINK,
    reason="Customer is ready to pay"
)

print("Ready to pay:")
print(execute_action(result))
print("-" * 40)



result = PolicyResult(
    action=Action.SCHEDULE_PAYMENT_REMINDER,
    reason="Customer wants to pay later"
)

result = PolicyResult(
    action=Action.UPDATE_PAYMENT_METHOD,
    reason="Customer needs to update their payment method"
)

result = PolicyResult(
    action=Action.SEND_FAILURE_EXPLANATION,
    reason="Customer asked why the payment failed"
)

result = PolicyResult(
    action=Action.NO_ACTION,
    reason="No action for this payment"
)

result = PolicyResult(
    action=Action.REVIEW,
    reason="Intent confidence is too low"
)
result = PolicyResult(
    action=Action.PAUSE_AND_ESCALATE,
    reason="Systemic payment failure detected"
)



print("Failure explanation:")
print(execute_action(result))

print("Payment delay:")
print(execute_action(result))
print("Update payment method:")
print(execute_action(result))
print(execute_action(result))
print(execute_action(result))

print(execute_action(result))
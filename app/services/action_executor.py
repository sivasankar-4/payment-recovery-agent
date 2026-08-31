from app.schemas.action import Action
from app.schemas.policyresult import PolicyResult


def execute_action(policy_result: PolicyResult):

     if policy_result.action == Action.SEND_PAYMENT_LINK:
        payment_link = "https://payment.example.com/pay/123"
        return payment_link

     if policy_result.action == Action.SCHEDULE_PAYMENT_REMINDER:
         return "Payment reminder scheduled."

     if policy_result.action == Action.UPDATE_PAYMENT_METHOD:
         return "Payment method update requested."

     if policy_result.action == Action.SEND_FAILURE_EXPLANATION:
         return "Payment failure explanation sent."

     if policy_result.action == Action.NO_ACTION:
         return "No action required."

     if policy_result.action == Action.REVIEW:
         return "Payment requires review."

     if policy_result.action == Action.PAUSE_AND_ESCALATE:
         return "Payment recovery paused and escalated."
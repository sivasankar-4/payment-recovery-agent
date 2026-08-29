from app.schemas.action import Action
from app.schemas.policyresult import PolicyResult
from app.schemas.intent import Intent

def evaluate_policy(systemic : bool,
                   retry_count : int,
                   recovery_score:float,
                   confidence: float,
                   intent,) -> PolicyResult:

          if systemic:
               return PolicyResult(
                   action=Action.PAUSE_AND_ESCALATE,
                   reason="systemic payment failure detected."
               )

          
          if retry_count >= 2:
                return PolicyResult(
                   action = Action.NO_ACTION,
                   reason="retry limit reached!!"
                )
          if confidence < 0.80:
                return PolicyResult(
                     action=Action.REVIEW,
                     reason="Intent confidence is below the minimum threshold."
                )
          if recovery_score >=80 and confidence >=0.80 and intent ==Intent.READY_TO_PAY:
                return PolicyResult(
                    action = Action.SEND_PAYMENT_LINK,
                    reason = "Customer is ready to pay"
                )

          if recovery_score >=80 and confidence >=0.80 and intent ==Intent.PAYMENT_DELAY:
                return PolicyResult(
                    action = Action.SCHEDULE_PAYMENT_REMINDER,
                    reason = "Customer wants to pay later"
                )

          if recovery_score < 80:

                return PolicyResult(
                  action=Action.NO_ACTION,
                  reason="Recovery score is below the minimum threshold."
            ) 
def decide_recovery(score,failure_reason,systemic,retry_count):
    if systemic:
        return "PAUSE_AND_ESCALATE"

    if retry_count >=2:
        return "NO_ACTION"
    
    if failure_reason == "CARD_EXPIRED":
        return "UPDATE_PAYMENT_METHOD"

    if score >= 80 and failure_reason == "INSUFFICIENT_FUNDS":
        return "RECOVER"

    if score >=80 and failure_reason == "TEMPORARY_FAILURE":
        return "RETRY_LATER"

    if score >=50:
        return "REVIEW"
    
    return "NO_ACTION"

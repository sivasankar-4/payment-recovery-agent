from app.services.recovery_decision import decide_recovery

tests = [

     {         
        "score" : 95,
        "failure_reason" : "INSUFFICIENT_FUNDS",
        "systemic" : False,
        "retry_count" : 0
     },

     {
         "score" : 60,
         "failure_reason" : "CARD_EXPIRED",
         "systemic" : False,
         "retry_count" : 0
     },

     {
        "score" : 95,
        "failure_reason" : "INSUFFICIENT_FUNDS",
        "systemic" : True,
        "retry_count" : 0
     },

     {
        "score" : 95,
        "failure_reason" : "INSUFFICIENT_FUNDS",
        "systemic" : False,
        "retry_count" : 2
     }
]

for test in tests:
    decision = decide_recovery(**test)

    print(
        f"{test} -> {decision}"
    )
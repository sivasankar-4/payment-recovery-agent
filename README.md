# Adaptive Revenue Recovery Agent

**Track:** AI Revenue Recovery — Razorpay Buildathon

An agent that decides if a failed payment is worth trying to recover, picks a safe recovery action, and knows when to stop.

## Why we're building this

When a payment fails, most systems simply try to send another payment link. That's not always the right thing to do.

For example:

- A UPI timeout on the first attempt? It may be worth retrying.
- A payment that has already been attempted twice? Stop rather than retry indefinitely.
- A customer says "I already paid, please check" — sending another payment link is the wrong response.
- A customer says "stop messaging me" — recovery should stop immediately.

The real problem isn't just sending payment reminders. It's deciding **when recovery makes sense, what action is safe, and when the system should stop.**

---

## How it works

The recovery agent follows a decision flow:

1. Receive a failed payment event.
2. Identify why the payment failed.
3. Look at the customer's recovery context and engagement.
4. Check whether the failure appears isolated or systemic.
5. Calculate a recovery score.
6. Select a recovery action.
7. Run the recommendation through hard policy rules.
8. Log the decision and continue or stop based on the result.

### Where we use AI, and where we don't

We're not using AI everywhere, on purpose.

Structured payment failure information such as `UPI_TIMEOUT` or `CARD_DECLINED` is handled using normal application logic. The payment system already provides this information, so using AI to interpret it would add unnecessary complexity.

AI is useful when the customer communicates in natural language and the intent needs to be interpreted.

For example:

- `"I already paid this morning, why are you asking again?"` → customer believes the payment was completed
- `"Please stop messaging me"` → customer wants to opt out
- `"I'll pay tomorrow"` → customer wants to pay later

This is where AI adds value: **understanding ambiguous customer intent.**

---

## AI recommends. Policy controls.

AI does not directly execute payment recovery actions.

The agent produces a recommendation, but the recommendation must pass through a policy layer before it can be used.

The agent can only choose from a fixed set of actions:

- `RETRY`
- `WAIT`
- `SEND_PAYMENT_LINK`
- `OFFER_ALTERNATIVE_METHOD`
- `PAUSE_AND_ESCALATE`
- `SCHEDULE_PAYMENT_REMINDER`
- `STOP`

It cannot invent arbitrary actions such as giving a discount or changing a payment amount.

This keeps the decision space controlled when dealing with real payments.

---

## Rules that cannot be overridden

These are hard safety conditions:

- If the payment has already been captured, stop.
- If the customer has opted out, stop.
- If the payment has already been attempted twice, stop.
- If the recommended action is not in the allowed action list, block it.
- Prevent duplicate recovery processing for the same payment at the same time.

The policy layer has the final say, regardless of what the AI recommends.

---

## Detecting systemic failures

Not every payment failure is an individual customer problem.

If multiple customers experience failures within a short time window, the system can identify the pattern as a potential systemic failure.

For example:

```text
Multiple customers fail payments
            ↓
Failures occur within a short window
            ↓
Systemic pattern detected
            ↓
Automatic recovery is paused
            ↓
Cases are escalated for investigation

Adaptive Revenue Recovery Agent

Track: AI Revenue Recovery — Razorpay Buildathon

An agent that decides if a failed payment is worth trying to recover, picks a safe way to do it, and knows when to stop.

Why we're building this

When a payment fails, most systems do one thing: send another payment link. That's not always right.

Some examples:

A UPI timeout on the first try? Worth a retry.
Card declined twice already, and we've already messaged the customer? Probably not worth bothering them again.
Customer says "I already paid, please check" — sending another link here is just wrong.
Customer says "stop messaging me" — we have to stop, no exceptions.

So the real question we're answering isn't "how do I send a payment reminder." It's: how do we recover failed payments without annoying customers or retrying blindly.

How it works

The agent doesn't just fire one message and move on. It loops:

Look at the payment failure (why did it fail)
Look at the customer's situation (did they say anything, are they active)
Check if this is a one-off issue or part of a bigger pattern (e.g. a bank having an outage)
Decide if trying to recover this is even worth it
Pick one action from a fixed list
Run it past some hard safety rules
Do it, watch what happens, and either stop or try the next step
Where we use AI, and where we don't

We're not using AI everywhere, on purpose.

Payment failure codes like UPI_TIMEOUT or CARD_DECLINED are handled with plain old code. There's nothing ambiguous about them, so throwing AI at it would just add cost and risk for no reason.

AI comes in when a customer says something in their own words and we need to figure out what they mean. Things like:

"I already paid this morning, why are you asking again?" → they think they've paid
"Please stop messaging me" → opt out, immediately
"I'll pay tomorrow" → they want to be asked later, not now

That's genuinely ambiguous input. That's where AI actually helps.

AI recommends. It doesn't get to act on its own.

This is the part we were most careful about. AI can suggest what to do, but every suggestion has to pass through a rules layer before anything actually happens. If the AI's suggestion breaks a rule, it gets blocked — no exceptions, no override.

The agent can only pick from a short, fixed list of actions:

RETRY
WAIT
SEND_PAYMENT_LINK
OFFER_ALTERNATIVE_METHOD
PAUSE_AND_ESCALATE
SCHEDULE_PAYMENT_REMINDER
STOP

It can't invent something like "give a 20% discount." That's not on the list, so it's not an option — which matters a lot when you're dealing with real money.

Rules that can't be overridden

These aren't suggestions, they're hard stops:

If the payment already went through, stop.
If the customer opted out, stop.
If we've already tried twice, stop.
If an action isn't on the allowed list, block it.
Don't run recovery twice on the same payment at the same time.
Spotting patterns, not just single failures

Sometimes a failure isn't really about the customer — it's a bank having issues, or a payment method breaking down for a lot of people at once. If we see a spike of similar failures clustered together (same bank, same method, short time window), we treat that differently. Instead of retrying blindly, we hold off and offer another payment method, because retrying into an outage just wastes everyone's time.

What's actually in this repo

Frontend — React, TypeScript, Vite, Tailwind. A dashboard for the merchant that shows open cases, a live log of every decision the agent made, and a banner if something looks systemic.

Backend — <!-- fill this in, e.g. FastAPI / Node / whatever you're using -->. It exposes two endpoints:

GET /api/payments — the payments, with status, why they failed, amount, customer info
GET /api/audit-logs — every decision the agent made, and why

The frontend checks both endpoints every 5 seconds so the dashboard stays current.

How we score "is this worth recovering"

Not a black box — just a simple weighted score:

score = (past success rate for this kind of failure)
      − (how many times we've already tried)
      + (any sign the customer is still engaged, like opening a link)
      − (how long it's been since the failure)

If the score is too low, we stop trying or just leave a payment link without following up.

Running this locally

Backend

<!-- fill in your actual setup steps and command -->

Frontend

bash
cd recovery-agent-frontend
npm install
npm run dev

The frontend expects the backend running on localhost:8000 with CORS already set up for it.

What we left out on purpose
Letting AI pick arbitrary actions like discounts — too risky when real money's involved.
Using AI to classify structured failure codes — the gateway already tells us what happened, no need to guess.
Unlimited retries — capped at 2, no matter what any recommendation says.
What we'd add next
<!-- fill in, e.g. detecting real bank outages from live failure rates, a voice channel, B2B receivables, promise-to-pay tracking -->

Team: <!-- fill in --> Built for Razorpay Buildathon, Track 03 — AI Revenue Recovery

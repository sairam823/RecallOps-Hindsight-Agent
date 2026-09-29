# RecallOps — 3-minute demo script

## 0:00–0:30 — Problem

**Say:**

"Production incidents repeat. Engineers may have solved a similar failure weeks ago, but the useful context is scattered across tickets, post-mortems and chat. RecallOps gives an incident-response agent persistent operational memory."

**Show:** RecallOps home screen.

## 0:30–1:10 — First incident

Enter:

```text
Service: payments-api
Severity: P1
Symptoms: HTTP 503, CPU 96%, high latency
Recent change: traffic increased after a campaign
Logs: upstream connection pool is saturated
```

Click **Investigate Incident**.

**Say:**

"At this point the agent only has the current incident and whatever prior memory is available. I want to teach it what actually happened."

## 1:10–1:40 — Resolution becomes memory

Enter:

```text
Root cause:
Backend capacity was insufficient for the traffic spike.

Actions attempted:
Restarted the API gateway. No improvement.

Successful fix:
Scaled payments-api replicas from 2 to 5.

Outcome:
503 rate returned to normal.
```

Click **Save resolution to Hindsight**.

**Say:**

"This is the important step. We are not just saving a chat transcript. We are retaining the operational outcome: what happened, what failed, what worked and why it mattered."

## 1:40–2:30 — Repeat the incident

Submit:

```text
Service: payments-api
Severity: P1
Symptoms: HTTP 503, CPU 94%, high latency
Recent change: another traffic spike
Logs: upstream connection pool is saturated
```

Click **Investigate Incident**.

Open **Recalled Experience**.

**Say:**

"Now Hindsight has found the earlier incident. The agent can use that experience to prioritize what to check. Notice that it should not blindly assume the old root cause is correct; it uses the old incident as evidence."

## 2:30–3:00 — Close

**Say:**

"The product loop is Incident, Recall, Reason, Resolve, Retain and Improve. The value is not simply that the agent remembers. The value is that remembered operational experience changes what it does next time."

Show the architecture diagram in the README or a prepared slide.

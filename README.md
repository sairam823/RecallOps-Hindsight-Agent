# RecallOps — Hindsight-Powered Incident Response Agent

RecallOps is an AI incident-response assistant that remembers previous production incidents, recalls relevant experience, and uses those lessons to make future troubleshooting more targeted.

## Why this project fits the challenge

The challenge asks for an AI agent that can remember, recall, and improve over time using Hindsight. RecallOps makes that loop the core product behavior:

**Incident → Recall → Reason → Resolution → Retain outcome → Better future response**

The demo is intentionally designed around a visible before/after:

- First incident: the agent has little/no relevant experience and gives general diagnostic guidance.
- Incident is resolved: the root cause, attempted actions, successful fix, and outcome are retained in Hindsight.
- Similar incident later: Hindsight recalls the previous experience and the agent produces a more targeted response.

## Product scope

**Persona:** DevOps / SRE engineer  
**Workflow:** Production incident triage  
**Value proposition:** Reduce repeated investigation by reusing organizational incident experience.

## Architecture

```text
                 ┌─────────────────────┐
                 │      Engineer       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Streamlit UI     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    RecallOps Agent  │
                 └───────┬───────┬─────┘
                         │       │
              ┌──────────▼─┐   ┌─▼──────────┐
              │  Hindsight │   │ Groq LLM   │
              │ retain/    │   │ reasoning  │
              │ recall     │   │            │
              └──────┬─────┘   └─────┬──────┘
                     │               │
                     └───────┬───────┘
                             ▼
                    ┌─────────────────┐
                    │ Incident result │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Retain outcome  │
                    │ into Hindsight  │
                    └─────────────────┘
```

## Hindsight integration

RecallOps uses the Hindsight Python client for the two central memory operations:

- `recall()` before generating incident guidance.
- `retain()` after an incident is resolved.

Hindsight's current client exposes `retain`, `recall`, and `reflect`; this project deliberately keeps the MVP centered on retain + recall so the memory loop is easy to understand during judging.

## Requirements

- Python 3.10+
- Hindsight instance (Cloud or self-hosted)
- Hindsight API key if your instance requires one
- Groq API key
- Streamlit

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

Copy `.env.example` to `.env` and fill in:

```env
GROQ_API_KEY=your_groq_key
GROQ_MODEL=openai/gpt-oss-120b

HINDSIGHT_BASE_URL=https://your-hindsight-endpoint
HINDSIGHT_API_KEY=your_hindsight_key
HINDSIGHT_BANK_ID=recallops-demo
```

Do not commit `.env`.

### 4. Start the app

```bash
streamlit run app.py
```

## First demo sequence

### Scenario A — teach the agent

Enter:

```text
Service: payments-api
Severity: P1
Symptoms: API returns HTTP 503. CPU is 96%. Latency has increased sharply.
Recent change: traffic increased after a campaign launch.
Logs: upstream connection pool is saturated.
```

Use the initial response to diagnose the incident.

Then close the incident with:

```text
Root cause: backend capacity was insufficient for the traffic spike.
Actions attempted: restarted API gateway; no improvement.
Successful fix: increased payments-api replicas from 2 to 5.
Outcome: HTTP 503 rate returned to normal.
```

Click **Save resolution to Hindsight**.

### Scenario B — test learning

Start a new incident with similar symptoms:

```text
Service: payments-api
Severity: P1
Symptoms: API returns HTTP 503. CPU is 94%. Latency is high.
Recent change: another traffic spike.
Logs: upstream connection pool is saturated.
```

The agent should now retrieve the earlier incident and explicitly use it as relevant prior experience.

## Important judging demo

Show these two outputs side by side:

**Before memory**
> Possible causes include backend overload, gateway failure, database exhaustion, or deployment issues. Check each layer.

**After Hindsight recall**
> A previous payments-api incident had the same 503 + high CPU + saturated connection-pool pattern. The gateway restart did not resolve it; scaling replicas from 2 to 5 did. Check backend capacity first.

The exact wording will depend on the model and recalled memories. The important behavior is that the second response is grounded in a real retained incident.

## Demo data

`data/sample_incidents.json` contains realistic synthetic incidents. These are synthetic examples for the prototype, not real production records.

## Safety

RecallOps is a decision-support prototype. It should not automatically execute production remediation commands. The engineer remains responsible for validating recommendations before taking operational action.

## Submission checklist

- [ ] GitHub repository is public and documented
- [ ] Hindsight integration works with real credentials
- [ ] Before/after memory demo recorded
- [ ] Live demo deployed
- [ ] 2–5 minute team video recorded
- [ ] Article written and published
- [ ] Each team member's social post prepared
- [ ] Hindsight usage explained clearly
- [ ] Screenshots / architecture diagram added

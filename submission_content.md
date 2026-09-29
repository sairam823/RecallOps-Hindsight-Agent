# RecallOps — Submission Content Pack

## Project title

**RecallOps: An Incident Response Agent That Learns From Previous Failures**

## One-line description

RecallOps helps DevOps engineers troubleshoot recurring production incidents by recalling previous incidents, their failed attempts, successful fixes and outcomes through Hindsight.

## Problem statement

Production incidents are time-sensitive, and the information needed to resolve them is often distributed across previous tickets, post-mortems and operational notes. A generic AI assistant can generate plausible troubleshooting steps, but it does not automatically carry organizational incident experience into the next incident.

## Solution

RecallOps creates a persistent memory loop around incident response:

1. Receive current incident evidence.
2. Recall relevant historical incidents through Hindsight.
3. Combine current evidence with prior experience.
4. Recommend focused investigation steps.
5. Capture the actual resolution.
6. Retain the outcome in Hindsight.
7. Use the accumulated experience during future incidents.

## What makes the memory visible

The same class of incident is demonstrated twice.

**Before:** the agent provides general diagnostic possibilities.

**After:** the agent recalls a previous incident and references its root cause, failed attempts and successful fix while prioritizing the next checks.

## Hindsight role

Hindsight is the persistent memory layer. RecallOps uses:

- `recall()` before reasoning about an incident.
- `retain()` after a resolution so the outcome can influence future incidents.

The project treats Hindsight as part of the core workflow rather than as a background database.

## Technical stack

- Python
- Streamlit
- Groq-compatible OpenAI client
- Hindsight Python client
- Synthetic incident data
- GitHub

## Important limitation

The prototype provides decision support. It does not automatically execute production remediation commands. A human engineer validates any recommended action.

## Suggested article title

**How I Built an Incident Agent That Remembers What Failed**

## Suggested LinkedIn post

Production incidents have a frustrating property: teams often solve the same class of problem more than once.

I built RecallOps around a simple idea: an incident-response agent should remember operational experience.

The loop is:

Incident → recall prior experience → reason → resolve → retain the outcome.

The useful part is the before/after behavior. Without relevant memory, the agent gives broad troubleshooting suggestions. After a previous incident is retained, a similar incident can bring back the earlier root cause, failed attempts and successful fix.

I used Hindsight as the persistent memory layer because the project needs more than a chat transcript—it needs reusable experience.

#AIAgents #Hindsight #AgentMemory #AI

## Video structure

1. 30 sec — Introduce the problem and product.
2. 30 sec — Show the generic response before useful memory exists.
3. 2 min — Resolve an incident, retain it, repeat a similar incident and show recall.
4. 30 sec — Explain how Hindsight changes the future response.

## Final checklist

- [ ] Real Hindsight credentials configured
- [ ] Historical incidents seeded or learned live
- [ ] Before/after behavior verified
- [ ] Screenshots captured
- [ ] README updated with actual screenshots and deployment URL
- [ ] GitHub repository cleaned
- [ ] Live demo tested
- [ ] Video recorded in 1080p
- [ ] Article edited to reflect actual implementation
- [ ] LinkedIn post edited to include the actual project URL

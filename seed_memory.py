"""
Optional helper to seed Hindsight with the synthetic incidents.

Run:
    python seed_memory.py

Use this before the first demo if you want RecallOps to have
historical incidents immediately.
"""

import json
from pathlib import Path

from dotenv import load_dotenv

from memory import HindsightMemory

load_dotenv()

incidents = json.loads(
    Path("data/sample_incidents.json").read_text(encoding="utf-8")
)

memory = HindsightMemory()

for incident in incidents:
    content = f"""
Incident ID: {incident['incident_id']}
Service: {incident['service']}
Severity: {incident['severity']}
Symptoms: {incident['symptoms']}
Recent change: {incident['recent_change']}
Root cause: {incident['root_cause']}
Actions attempted: {', '.join(incident['attempted_actions'])}
Successful fix: {incident['successful_fix']}
Outcome: {incident['outcome']}
""".strip()

    memory.client.retain(
        bank_id=memory.bank_id,
        content=content,
        context="synthetic historical production incident",
        document_id=incident["incident_id"],
        metadata={
            "source": "recallops-seed",
            "incident_id": incident["incident_id"],
            "status": "resolved",
        },
    )

    print(f"Retained {incident['incident_id']}")

print("Seed complete.")

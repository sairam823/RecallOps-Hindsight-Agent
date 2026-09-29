import os
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agent import RecallOpsAgent

load_dotenv()

st.set_page_config(
    page_title="RecallOps",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 RecallOps")
st.caption("Incident response that remembers what your team learned last time.")

if "last_result" not in st.session_state:
    st.session_state.last_result = None

with st.sidebar:
    st.header("System")
    hindsight_ok = bool(os.getenv("HINDSIGHT_BASE_URL"))
    groq_ok = bool(os.getenv("GROQ_API_KEY"))

    st.write("Hindsight:", "Connected" if hindsight_ok else "Not configured")
    st.write("Groq:", "Configured" if groq_ok else "Not configured")

    st.divider()
    st.markdown(
        """
**Core loop**

`Incident → Recall → Reason → Resolve → Retain → Improve`
"""
    )

tab_incident, tab_memory, tab_demo = st.tabs(
    ["🚨 Incident Triage", "🧠 Recalled Experience", "🎬 Demo Guide"]
)

with tab_incident:
    st.subheader("Describe the current incident")

    incident = st.text_area(
        "Incident details",
        height=190,
        placeholder=(
            "Example:\n"
            "Service: payments-api\n"
            "Severity: P1\n"
            "Symptoms: HTTP 503, CPU 96%, high latency\n"
            "Recent change: traffic increased\n"
            "Logs: upstream connection pool is saturated"
        ),
    )

    if st.button("Investigate Incident", type="primary", use_container_width=True):
        if not incident.strip():
            st.warning("Enter the incident details first.")
        else:
            try:
                with st.spinner("Recalling prior incidents and analyzing current evidence..."):
                    agent = RecallOpsAgent()
                    st.session_state.last_result = agent.investigate(incident)
            except Exception as exc:
                st.error(f"Agent error: {exc}")
                st.info(
                    "Check GROQ_API_KEY, HINDSIGHT_BASE_URL, HINDSIGHT_API_KEY, "
                    "and HINDSIGHT_BANK_ID in .env."
                )

    if st.session_state.last_result:
        st.markdown("### Agent assessment")
        st.markdown(st.session_state.last_result["answer"])

with tab_memory:
    st.subheader("What Hindsight recalled")

    result = st.session_state.last_result
    if not result:
        st.info("Run an incident investigation first.")
    else:
        memories = result["memories"]
        if not memories:
            st.warning("No relevant prior experience was returned for this incident.")
        else:
            st.success(f"{len(memories)} relevant memory result(s) recalled.")
            for idx, memory in enumerate(memories, 1):
                with st.expander(
                    f"Memory {idx} · {memory.get('type', 'unknown')} · "
                    f"{memory.get('context', 'no context')}"
                ):
                    st.write(memory.get("text", ""))

    st.divider()
    st.subheader("Save the resolved incident")

    resolved_incident = st.text_area(
        "Incident / symptoms",
        key="resolved_incident",
        height=100,
    )
    root_cause = st.text_area("Root cause", key="root_cause")
    attempted = st.text_area(
        "Actions attempted (include failed attempts)",
        key="attempted",
    )
    successful_fix = st.text_area("Successful fix", key="successful_fix")
    outcome = st.text_area("Outcome", key="outcome")

    if st.button("Save resolution to Hindsight", use_container_width=True):
        if not all(
            [
                resolved_incident.strip(),
                root_cause.strip(),
                successful_fix.strip(),
                outcome.strip(),
            ]
        ):
            st.warning("Fill incident, root cause, successful fix, and outcome.")
        else:
            try:
                with st.spinner("Retaining the incident outcome in Hindsight..."):
                    agent = RecallOpsAgent()
                    incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
                    agent.save_resolution(
                        incident=resolved_incident,
                        root_cause=root_cause,
                        attempted_actions=attempted,
                        successful_fix=successful_fix,
                        outcome=outcome,
                        incident_id=incident_id,
                    )
                st.success(f"{incident_id} retained in Hindsight.")
            except Exception as exc:
                st.error(f"Could not retain the incident: {exc}")

with tab_demo:
    st.subheader("60-second judge demo")

    st.markdown(
        """
### 1 — Before memory
Enter a 503 incident and show that the agent has only the current evidence.

### 2 — Teach RecallOps
Resolve the incident and save:
- root cause
- failed attempts
- successful fix
- outcome

### 3 — Repeat the incident
Submit a similar 503 incident.

### 4 — Show the difference
Open **Recalled Experience** and show the prior incident.

### 5 — Explain the point
The agent is no longer responding only from the current prompt. It is using retained operational experience to change the investigation.
"""
    )

    st.code(
        """First incident
503 + high CPU
        ↓
Resolve
Backend overloaded
        ↓
Retain in Hindsight
        ↓
Second incident
503 + high CPU
        ↓
Recall previous experience
        ↓
Targeted investigation""",
        language="text",
    )

    st.info(
        "Do not claim that Hindsight proves the same root cause. "
        "Present the recalled incident as prior evidence that helps prioritize investigation."
    )

# RecallOps Architecture

```mermaid
flowchart TD
    U[DevOps / SRE Engineer] --> UI[Streamlit Incident UI]
    UI --> A[RecallOps Agent]
    A --> R[Hindsight Recall]
    R --> M[Relevant Incident Memories]
    M --> A
    A --> L[Groq LLM Reasoning]
    L --> O[Investigation Guidance]
    O --> U
    U --> C[Incident Resolution]
    C --> T[Hindsight Retain]
    T --> R
```

## Memory loop

```text
Current incident
      ↓
Hindsight recall
      ↓
Prior operational experience
      ↓
LLM reasoning
      ↓
Targeted guidance
      ↓
Human validates and resolves
      ↓
Resolution outcome
      ↓
Hindsight retain
      ↓
Future incident recall
```

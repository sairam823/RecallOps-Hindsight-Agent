import os

from openai import OpenAI

from memory import HindsightMemory
from prompts import SYSTEM_PROMPT, build_user_prompt


class RecallOpsAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Add it to .env.")

        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        self.llm = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.memory = HindsightMemory()

    def investigate(self, incident: str):
        memories = self.memory.recall(incident)

        memory_text = "\n\n".join(
            [
                f"[Memory {i + 1}] {m['text']}"
                for i, m in enumerate(memories)
                if m["text"]
            ]
        )

        response = self.llm.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(incident, memory_text),
                },
            ],
        )

        answer = response.choices[0].message.content
        return {
            "answer": answer,
            "memories": memories,
        }

    def save_resolution(
        self,
        incident: str,
        root_cause: str,
        attempted_actions: str,
        successful_fix: str,
        outcome: str,
        incident_id: str,
    ):
        return self.memory.retain_resolution(
            incident=incident,
            root_cause=root_cause,
            attempted_actions=attempted_actions,
            successful_fix=successful_fix,
            outcome=outcome,
            incident_id=incident_id,
        )

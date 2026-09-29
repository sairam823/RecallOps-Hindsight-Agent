import os
from typing import Any

from hindsight_client import Hindsight


class HindsightMemory:
    """Thin wrapper around Hindsight for the RecallOps workflow."""

    def __init__(self) -> None:
        base_url = os.getenv("HINDSIGHT_BASE_URL", "").strip()
        api_key = os.getenv("HINDSIGHT_API_KEY", "").strip()
        self.bank_id = os.getenv("HINDSIGHT_BANK_ID", "recallops-demo").strip()

        if not base_url:
            raise RuntimeError(
                "HINDSIGHT_BASE_URL is missing. Add it to .env before running RecallOps."
            )

        kwargs = {"base_url": base_url}
        if api_key:
            kwargs["api_key"] = api_key

        self.client = Hindsight(**kwargs)

    def recall(self, query: str, max_tokens: int = 2500) -> list[dict[str, Any]]:
        response = self.client.recall(
            bank_id=self.bank_id,
            query=query,
            max_tokens=max_tokens,
        )

        output = []
        for item in getattr(response, "results", []) or []:
            output.append(
                {
                    "id": getattr(item, "id", ""),
                    "text": getattr(item, "text", ""),
                    "type": getattr(item, "type", ""),
                    "context": getattr(item, "context", ""),
                    "metadata": getattr(item, "metadata", {}) or {},
                }
            )
        return output

    def retain_resolution(
        self,
        incident: str,
        root_cause: str,
        attempted_actions: str,
        successful_fix: str,
        outcome: str,
        incident_id: str,
    ):
        content = f"""
RecallOps resolved incident {incident_id}.

Current incident:
{incident}

Root cause:
{root_cause}

Actions attempted:
{attempted_actions}

Successful fix:
{successful_fix}

Outcome:
{outcome}
""".strip()

        return self.client.retain(
            bank_id=self.bank_id,
            content=content,
            context="production incident resolution",
            document_id=incident_id,
            metadata={
                "source": "recallops",
                "incident_id": incident_id,
                "status": "resolved",
            },
        )

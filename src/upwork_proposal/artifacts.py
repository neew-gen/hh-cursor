from __future__ import annotations

from pathlib import Path

ARTIFACTS_DIR = Path("artifacts/upwork-proposal")


def resolve_proposal_plan_path(job_slug: str) -> Path:
    return ARTIFACTS_DIR / f"{job_slug}.yaml"


def resolve_report_path(job_slug: str) -> Path:
    return ARTIFACTS_DIR / f"{job_slug}-report.yaml"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR

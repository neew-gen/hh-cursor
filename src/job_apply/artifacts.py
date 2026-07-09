from __future__ import annotations

from pathlib import Path

ARTIFACTS_DIR = Path("artifacts/job-apply")


def resolve_application_plan_path(vacancy_slug: str) -> Path:
    return ARTIFACTS_DIR / f"{vacancy_slug}.yaml"


def resolve_report_path(vacancy_slug: str) -> Path:
    return ARTIFACTS_DIR / f"{vacancy_slug}-report.yaml"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR

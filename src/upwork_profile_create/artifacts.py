from __future__ import annotations

from pathlib import Path

from resume_profile.slug import slugify_target_role

ARTIFACTS_DIR = Path("artifacts/upwork-profile-create")


def resolve_fill_plan_path(profile_title: str) -> Path:
    slug = slugify_target_role(profile_title)
    return ARTIFACTS_DIR / f"{slug}.yaml"


def resolve_report_path(profile_title: str) -> Path:
    slug = slugify_target_role(profile_title)
    return ARTIFACTS_DIR / f"{slug}-report.yaml"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR

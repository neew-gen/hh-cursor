from __future__ import annotations

from typing import Any

from freelancer_core.models import WorkExperienceEntry
from upwork_profile.models import GapField, UpworkProfile
from upwork_profile.schema import MVP_GAP_FIELD_IDS, gap_field


def _has_valid_experience_entry(entry: WorkExperienceEntry) -> bool:
    return bool(
        entry.company.strip()
        and entry.position.strip()
        and entry.start_date.strip()
        and entry.description.strip()
    )


def compute_gaps(
    profile: UpworkProfile,
    mvp_only: bool = True,
    meta: dict[str, Any] | None = None,
) -> list[GapField]:
    gaps: list[GapField] = []
    meta = meta or {}

    if not profile.profile_title.strip():
        gaps.append(gap_field("profile_title"))

    if not profile.overview.strip():
        gaps.append(gap_field("overview"))

    if not (profile.hourly_rate or "").strip():
        gaps.append(gap_field("hourly_rate"))

    if not profile.skills:
        gaps.append(gap_field("skills"))

    if not profile.work_experience_status.strip():
        gaps.append(gap_field("work_experience_status"))
    elif profile.work_experience_status == "has_experience":
        valid_entries = [e for e in profile.work_experience if _has_valid_experience_entry(e)]
        if not valid_entries:
            gaps.append(gap_field("work_experience"))
    elif profile.work_experience_status not in ("none", "has_experience"):
        gaps.append(gap_field("work_experience_status"))

    has_education = any(e.institution.strip() for e in profile.education)
    if not has_education:
        gaps.append(gap_field("education", required=False))

    if not profile.portfolio_links:
        gaps.append(gap_field("portfolio_links", required=False))

    if mvp_only:
        allowed = set(MVP_GAP_FIELD_IDS)
        gaps = [g for g in gaps if g.field_id in allowed]

    seen: set[str] = set()
    unique_gaps: list[GapField] = []
    for gap in gaps:
        if gap.field_id in seen:
            continue
        seen.add(gap.field_id)
        unique_gaps.append(gap)
    return unique_gaps


def is_complete(profile: UpworkProfile, meta: dict[str, Any] | None = None) -> bool:
    return len(completeness_errors(profile, meta=meta)) == 0


def completeness_errors(profile: UpworkProfile, meta: dict[str, Any] | None = None) -> list[str]:
    errors = []
    for gap in compute_gaps(profile, meta=meta):
        if gap.required:
            errors.append(f"Missing required field: {gap.field_id}")
    return errors

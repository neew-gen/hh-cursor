from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resume_profile.models import ResumeProfile
from resume_profile.writer import profile_from_dict

from resume_create.loader import load_intelligence, load_profile, resolve_target_url
from resume_create.models import FillPlan, FillPlanMeta, RewriteApplied

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/resume-intelligence.md")


def compose_fill_plan(
    profile_path: str | Path,
    draft_path: str | Path,
    fill_mode: str,
    intelligence_path: str | Path | None = None,
) -> FillPlan:
    source_profile = load_profile(profile_path)
    draft_data = json.loads(Path(draft_path).read_text(encoding="utf-8"))
    merged_profile = _merge_draft_into_profile(source_profile, draft_data)

    intel_path = Path(intelligence_path) if intelligence_path else INTELLIGENCE_DEFAULT_PATH
    intelligence = load_intelligence(intel_path if intel_path.is_file() else None)

    rewrite_meta = draft_data.get("rewrite_applied") or {}
    citations = draft_data.get("intelligence_citations") or intelligence.source_ids

    meta = FillPlanMeta(
        composed_at=datetime.now(timezone.utc).isoformat(),
        source_profile=str(profile_path),
        intelligence_path=str(intel_path) if intel_path.is_file() else None,
        intelligence_freshness=intelligence.generated_at,
        fill_mode=fill_mode,
        target_url=resolve_target_url(fill_mode, merged_profile.resume_link),
        rewrite_applied=RewriteApplied(
            about_me=bool(rewrite_meta.get("about_me", False)),
            work_experience_descriptions=bool(
                rewrite_meta.get("work_experience_descriptions", False)
            ),
        ),
        intelligence_citations=list(citations),
    )
    return FillPlan(profile=merged_profile, meta=meta)


def _merge_draft_into_profile(
    source_profile: ResumeProfile,
    draft_data: dict[str, Any],
) -> ResumeProfile:
    base = profile_from_dict(_profile_to_merge_dict(source_profile))

    if "about_me" in draft_data and draft_data["about_me"] is not None:
        base.about_me = draft_data["about_me"]

    draft_experience = draft_data.get("work_experience")
    if isinstance(draft_experience, list) and draft_experience:
        if len(draft_experience) != len(base.work_experience):
            raise ValueError(
                "work_experience count in draft must match source profile."
            )
        for index, entry in enumerate(draft_experience):
            if "description" in entry and entry["description"] is not None:
                base.work_experience[index].description = entry["description"]

    return base


def _profile_to_merge_dict(profile: ResumeProfile) -> dict[str, Any]:
    from resume_profile.writer import profile_to_dict

    return copy.deepcopy(profile_to_dict(profile))

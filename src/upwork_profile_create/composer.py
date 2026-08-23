from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from upwork_profile_create.loader import load_intelligence, load_profile, profile_from_dict, profile_to_dict, resolve_target_url
from upwork_profile_create.models import FillPlan, FillPlanMeta, RewriteApplied, UpworkProfile

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/upwork-intelligence.md")


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
        target_url=resolve_target_url(fill_mode, merged_profile.profile_link),
        rewrite_applied=RewriteApplied(
            overview=bool(rewrite_meta.get("overview", False)),
            profile_title=bool(rewrite_meta.get("profile_title", False)),
            work_experience_descriptions=bool(
                rewrite_meta.get("work_experience_descriptions", False)
            ),
            skills_tags=bool(rewrite_meta.get("skills_tags", False)),
        ),
        intelligence_citations=list(citations),
    )
    return FillPlan(profile=merged_profile, meta=meta)


def _merge_draft_into_profile(
    source_profile: UpworkProfile,
    draft_data: dict[str, Any],
) -> UpworkProfile:
    base = profile_from_dict(_profile_to_merge_dict(source_profile))

    if "overview" in draft_data and draft_data["overview"] is not None:
        base.overview = draft_data["overview"]

    if "profile_title" in draft_data and draft_data["profile_title"] is not None:
        base.profile_title = draft_data["profile_title"]

    if "skills" in draft_data and draft_data["skills"] is not None:
        base.skills = [str(item) for item in draft_data["skills"]]

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


def _profile_to_merge_dict(profile: UpworkProfile) -> dict[str, Any]:
    return copy.deepcopy(profile_to_dict(profile))

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from resume_create.loader import load_intelligence
from job_apply.loader import load_profile, load_vacancy_extract
from job_apply.models import ApplicationPlan, CoverLetter

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/resume-intelligence.md")


def compose_application_plan(
    profile_path: str | Path,
    vacancy_path: str | Path,
    draft_path: str | Path,
    intelligence_path: str | Path | None = None,
) -> ApplicationPlan:
    profile = load_profile(profile_path)
    vacancy = load_vacancy_extract(vacancy_path)
    draft_data = json.loads(Path(draft_path).read_text(encoding="utf-8"))

    cover_text = str(draft_data.get("cover_letter_text", "")).strip()
    if not cover_text:
        raise ValueError("cover_letter_text is required in draft JSON.")

    language = str(draft_data.get("language") or "ru")
    intel_path = Path(intelligence_path) if intelligence_path else INTELLIGENCE_DEFAULT_PATH
    intelligence = load_intelligence(intel_path if intel_path.is_file() else None)

    citations = draft_data.get("intelligence_citations") or intelligence.source_ids
    limitations = list(intelligence.limitations)
    if not intelligence.what_to_write and not intelligence.how_to_build_resume:
        limitations.append("Default cover letter rules used; resume-intelligence not available.")

    return ApplicationPlan(
        composed_at=datetime.now(timezone.utc).isoformat(),
        vacancy=vacancy,
        source_profile=str(profile_path),
        target_role=profile.target_role,
        resume_match_hint=profile.target_role,
        cover_letter=CoverLetter(
            text=cover_text,
            language=language,
            char_count=len(cover_text),
        ),
        rewrite_applied=bool(draft_data.get("rewrite_applied", True)),
        intelligence_path=str(intel_path) if intel_path.is_file() else None,
        intelligence_freshness=intelligence.generated_at,
        intelligence_citations=list(citations),
        limitations=limitations,
    )

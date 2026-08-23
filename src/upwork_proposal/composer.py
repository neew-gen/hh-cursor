from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from upwork_proposal.loader import INTELLIGENCE_DEFAULT_PATH, load_intelligence, load_job_extract, load_profile
from upwork_proposal.models import ContractTerms, ProposalCoverLetter, ProposalPlan, ScreeningAnswer


def compose_proposal_plan(
    profile_path: str | Path,
    job_path: str | Path,
    draft_path: str | Path,
    intelligence_path: str | Path | None = None,
) -> ProposalPlan:
    profile = load_profile(profile_path)
    job = load_job_extract(job_path)
    draft_data = json.loads(Path(draft_path).read_text(encoding="utf-8"))

    cover_text = str(draft_data.get("cover_letter_text", "")).strip()
    if not cover_text:
        raise ValueError("cover_letter_text is required in draft JSON.")

    language = str(draft_data.get("language") or "en")
    intel_path = Path(intelligence_path) if intelligence_path else INTELLIGENCE_DEFAULT_PATH
    intelligence = load_intelligence(intel_path if intel_path.is_file() else None)

    citations = draft_data.get("intelligence_citations") or intelligence.source_ids
    limitations = list(intelligence.limitations)
    if not intelligence.what_to_write and not intelligence.how_to_build_profile:
        limitations.append("Default proposal rules used; upwork-intelligence not available.")

    screening_answers = _parse_screening_answers(draft_data)
    contract_terms = _parse_contract_terms(draft_data)

    return ProposalPlan(
        composed_at=datetime.now(timezone.utc).isoformat(),
        job=job,
        source_profile=str(profile_path),
        target_role=profile.profile_title,
        profile_match_hint=profile.profile_title,
        cover_letter=ProposalCoverLetter(
            text=cover_text,
            language=language,
            char_count=len(cover_text),
        ),
        screening_answers=screening_answers,
        contract_terms=contract_terms,
        rewrite_applied=bool(draft_data.get("rewrite_applied", True)),
        intelligence_path=str(intel_path) if intel_path.is_file() else None,
        intelligence_freshness=intelligence.generated_at,
        intelligence_citations=list(citations),
        limitations=limitations,
    )


def _parse_screening_answers(draft_data: dict) -> list[ScreeningAnswer]:
    answers: list[ScreeningAnswer] = []
    for item in draft_data.get("screening_answers") or []:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        if question or answer:
            answers.append(ScreeningAnswer(question=question, answer=answer))
    return answers


def _parse_contract_terms(draft_data: dict) -> ContractTerms | None:
    raw = draft_data.get("contract_terms")
    if not raw or not isinstance(raw, dict):
        return None

    milestones = [str(item) for item in raw.get("milestones") or []]
    connects = raw.get("connects_required")
    connects_required = int(connects) if connects is not None else None

    return ContractTerms(
        bid_type=_optional_str(raw.get("bid_type")),
        hourly_rate=_optional_str(raw.get("hourly_rate")),
        fixed_price=_optional_str(raw.get("fixed_price")),
        duration=_optional_str(raw.get("duration")),
        weekly_hours=_optional_str(raw.get("weekly_hours")),
        milestones=milestones,
        connects_required=connects_required,
    )


def _optional_str(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None

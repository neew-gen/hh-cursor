from __future__ import annotations

import re
from pathlib import Path

from upwork_proposal.loader import load_profile
from upwork_proposal.models import ProposalPlan

MIN_COVER_LETTER_LENGTH = 300
MAX_COVER_LETTER_LENGTH = 5000


def validate_proposal_plan(
    plan: ProposalPlan,
    profile_path: str | Path,
) -> list[str]:
    profile = load_profile(profile_path)
    errors: list[str] = []

    if not plan.job.url.strip():
        errors.append("job.url is empty.")
    if not plan.job.title.strip():
        errors.append("job.title is empty.")
    if not plan.cover_letter.text.strip():
        errors.append("cover_letter.text is empty.")

    if plan.cover_letter.char_count != len(plan.cover_letter.text):
        errors.append("cover_letter.char_count does not match text length.")

    text_len = len(plan.cover_letter.text)
    if text_len < MIN_COVER_LETTER_LENGTH:
        errors.append(
            f"cover_letter.text is shorter than minimum ({MIN_COVER_LETTER_LENGTH} chars)."
        )
    if text_len > MAX_COVER_LETTER_LENGTH:
        errors.append(
            f"cover_letter.text exceeds maximum ({MAX_COVER_LETTER_LENGTH} chars)."
        )

    if _normalize_text(plan.target_role) != _normalize_text(profile.profile_title):
        errors.append("target_role differs from source profile.")

    errors.extend(
        _validate_employer_mentions(plan.cover_letter.text, profile, plan.job.client)
    )
    errors.extend(_validate_skill_mentions(plan.cover_letter.text, profile))
    errors.extend(_validate_screening_answers(plan))

    return errors


def validate_proposal_plan_file(
    plan_path: str | Path,
    profile_path: str | Path,
) -> list[str]:
    from upwork_proposal.writer import load_proposal_plan

    plan = load_proposal_plan(plan_path)
    return validate_proposal_plan(plan, profile_path)


def _validate_screening_answers(plan: ProposalPlan) -> list[str]:
    errors: list[str] = []
    expected = [q.strip() for q in plan.job.screening_questions if q.strip()]
    if not expected:
        return errors

    answered = {a.question.strip(): a.answer.strip() for a in plan.screening_answers}
    for question in expected:
        if question not in answered or not answered[question]:
            errors.append(f"screening question unanswered: {question}")
    return errors


def _validate_employer_mentions(text: str, profile, job_client: str = "") -> list[str]:
    errors: list[str] = []
    profile_companies = {
        _normalize_company(e.company)
        for e in profile.work_experience
        if e.company and e.company.strip()
    }
    allowed = set(profile_companies)
    if job_client:
        allowed.add(_normalize_company(job_client))

    mentioned = _extract_employer_phrases(text)
    unknown = {name for name in mentioned if name not in allowed}
    if unknown:
        errors.append(
            "cover_letter mentions employers not in profile: "
            + ", ".join(sorted(unknown))
        )
    return errors


EMPLOYER_CONTEXT_PATTERNS = [
    re.compile(r"worked\s+(?:at|for)\s+([^,\.\n;]+)", re.IGNORECASE),
]


def _extract_employer_phrases(text: str) -> set[str]:
    mentioned: set[str] = set()
    for pattern in EMPLOYER_CONTEXT_PATTERNS:
        for match in pattern.finditer(text):
            candidate = _normalize_company(match.group(1))
            if len(candidate) >= 3:
                mentioned.add(candidate)
    return mentioned


def _validate_skill_mentions(text: str, profile) -> list[str]:
    errors: list[str] = []
    allowed_skills = _collect_allowed_skills(profile)
    if not allowed_skills:
        return errors

    mentioned_skills = _extract_mentioned_skills(text, allowed_skills)
    unknown = mentioned_skills - allowed_skills
    if unknown:
        errors.append(
            "cover_letter mentions skills not in profile: "
            + ", ".join(sorted(unknown))
        )
    return errors


def _collect_allowed_skills(profile) -> set[str]:
    skills: set[str] = set()
    for skill in profile.skills:
        if skill:
            skills.add(_normalize_text(skill))

    for experience in profile.work_experience:
        for match in re.finditer(
            r"(?:stack|tech)\s*:\s*([^\n]+)",
            experience.description or "",
            re.IGNORECASE,
        ):
            for part in re.split(r"[,;/|]", match.group(1)):
                token = _normalize_text(part)
                if len(token) >= 2:
                    skills.add(token)

    return skills


def _extract_mentioned_skills(text: str, allowed_skills: set[str]) -> set[str]:
    mentioned: set[str] = set()
    normalized_text = _normalize_text(text)
    for skill in allowed_skills:
        if len(skill) < 2:
            continue
        if re.search(rf"\b{re.escape(skill)}\b", normalized_text):
            mentioned.add(skill)
    return mentioned


def _normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value.strip().lower())


def _normalize_company(value: str) -> str:
    text = _normalize_text(value)
    text = re.sub(r"[«»\"'()]", "", text)
    return text

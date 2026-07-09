from __future__ import annotations

import re
from pathlib import Path

from resume_profile.models import ResumeProfile

from resume_create.loader import load_profile
from resume_create.models import FillPlan

MONTH_MAP = {
    "январь": "01",
    "февраль": "02",
    "март": "03",
    "апрель": "04",
    "май": "05",
    "июнь": "06",
    "июль": "07",
    "август": "08",
    "сентябрь": "09",
    "октябрь": "10",
    "ноябрь": "11",
    "декабрь": "12",
}


def validate_fill_plan(fill_plan: FillPlan, profile_path: str | Path) -> list[str]:
    source = load_profile(profile_path)
    errors: list[str] = []

    if not fill_plan.profile.target_role.strip():
        errors.append("target_role is empty.")

    errors.extend(_compare_profiles(source, fill_plan.profile))
    return errors


def validate_fill_plan_file(fill_plan_path: str | Path, profile_path: str | Path) -> list[str]:
    from resume_create.writer import load_fill_plan

    fill_plan = load_fill_plan(fill_plan_path)
    return validate_fill_plan(fill_plan, profile_path)


def _compare_profiles(source: ResumeProfile, candidate: ResumeProfile) -> list[str]:
    errors: list[str] = []

    if _normalize_text(source.target_role) != _normalize_text(candidate.target_role):
        errors.append("target_role differs from source profile.")

    source_companies = [_normalize_text(e.company) for e in source.work_experience]
    candidate_companies = [_normalize_text(e.company) for e in candidate.work_experience]
    if source_companies != candidate_companies:
        errors.append("work_experience companies differ from source profile.")

    source_positions = [_normalize_text(e.position) for e in source.work_experience]
    candidate_positions = [_normalize_text(e.position) for e in candidate.work_experience]
    if source_positions != candidate_positions:
        errors.append("work_experience positions differ from source profile.")

    for index, (src, cand) in enumerate(zip(source.work_experience, candidate.work_experience)):
        if normalize_date(src.start_date) != normalize_date(cand.start_date):
            errors.append(f"work_experience[{index}].start_date differs from source profile.")
        if normalize_date(src.end_date) != normalize_date(cand.end_date):
            errors.append(f"work_experience[{index}].end_date differs from source profile.")

    source_skills = sorted(_normalize_text(s.name) for s in source.skills_hard)
    candidate_skills = sorted(_normalize_text(s.name) for s in candidate.skills_hard)
    if source_skills != candidate_skills:
        errors.append("skills.hard names differ from source profile.")

    source_institutions = [_normalize_text(e.institution) for e in source.education]
    candidate_institutions = [_normalize_text(e.institution) for e in candidate.education]
    if source_institutions != candidate_institutions:
        errors.append("education institutions differ from source profile.")

    return errors


def _normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value.strip().lower())


def normalize_date(value: str | None) -> str:
    if value is None:
        return ""
    text = value.strip().lower()
    if not text:
        return ""

    iso_match = re.match(r"^(\d{4})-(\d{2})$", text)
    if iso_match:
        return f"{iso_match.group(2)}.{iso_match.group(1)}"

    dot_match = re.match(r"^(\d{2})\.(\d{4})$", text)
    if dot_match:
        return f"{dot_match.group(1)}.{dot_match.group(2)}"

    for month_name, month_num in MONTH_MAP.items():
        pattern = rf"^{month_name}\s+(\d{{4}})$"
        match = re.match(pattern, text)
        if match:
            return f"{month_num}.{match.group(1)}"

    return text

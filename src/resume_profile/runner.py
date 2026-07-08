from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from resume_profile.artifacts import load_artifact, resolve_artifact_path, write_artifact_bundle
from resume_profile.draft import (
    SKILLS_MODE_APPEND,
    SKILLS_MODE_NEW,
    load_draft,
    merge_skill_entries,
    save_draft,
)
from resume_profile.gaps import completeness_errors, compute_gaps, is_complete
from resume_profile.models import ResumeProfile
from resume_profile.questionnaire import build_ask_options, gap_question
from resume_profile.writer import finalize_profile


def load_profile_json(path: str | Path) -> ResumeProfile:
    profile, _meta = load_draft(path)
    return profile


def merge_extracted_profile(base: ResumeProfile, incoming: ResumeProfile) -> ResumeProfile:
    merged = deepcopy(base)

    if incoming.input_mode:
        merged.input_mode = incoming.input_mode
    if incoming.resume_link:
        merged.resume_link = incoming.resume_link
    if incoming.target_role.strip():
        merged.target_role = incoming.target_role
    if incoming.specializations:
        merged.specializations = incoming.specializations
    if incoming.work_experience_status.strip():
        merged.work_experience_status = incoming.work_experience_status
    if incoming.work_experience:
        merged.work_experience = incoming.work_experience
    if incoming.skills_hard:
        merged.skills_hard = incoming.skills_hard
    if incoming.skills_soft:
        merged.skills_soft = incoming.skills_soft
    if incoming.education:
        merged.education = incoming.education
        merged.no_formal_education = False
    elif incoming.no_formal_education:
        merged.education = []
        merged.no_formal_education = True
    if (incoming.about_me or "").strip():
        merged.about_me = incoming.about_me
    if incoming.work_preferences is not None:
        merged.work_preferences = incoming.work_preferences
    if incoming.languages:
        merged.languages = incoming.languages
    if incoming.additional_education:
        merged.additional_education = incoming.additional_education
    if incoming.portfolio_links:
        merged.portfolio_links = incoming.portfolio_links
    if incoming.personal_links:
        merged.personal_links = incoming.personal_links
    if incoming.limitations:
        merged.limitations = incoming.limitations

    merged.sources = incoming.sources
    return merged


def write_profile_artifact(
    profile: ResumeProfile,
    output_path: str | Path | None = None,
    *,
    meta: dict[str, Any] | None = None,
) -> Path:
    finalized = finalize_profile(profile)
    if meta and meta.get("skills_mode") == SKILLS_MODE_APPEND and meta.get("base_skills"):
        from resume_profile.models import SkillEntry

        base = [
            SkillEntry(
                name=item["name"],
                level=item.get("level", "medium"),
                provenance=item.get("provenance", "from_user_answer"),
            )
            for item in meta["base_skills"]
        ]
        finalized.skills_hard = merge_skill_entries(
            base,
            finalized.skills_hard,
            mode=SKILLS_MODE_APPEND,
        )

    errors = completeness_errors(finalized, meta=meta)
    if errors:
        raise ValueError("; ".join(errors))

    path = Path(output_path) if output_path else resolve_artifact_path(finalized.target_role)
    return write_artifact_bundle(finalized, path)


def list_gaps(profile: ResumeProfile, meta: dict[str, Any] | None = None) -> list[dict[str, object]]:
    meta = meta or {}
    items: list[dict[str, object]] = []
    for gap in compute_gaps(profile, meta=meta):
        items.append(
            {
                "field_id": gap.field_id,
                "question": gap_question(gap.field_id, profile, meta=meta),
                "required": gap.required,
                "ask_options": build_ask_options(gap.field_id, profile),
            }
        )
    return items


def profile_is_complete(profile: ResumeProfile, meta: dict[str, Any] | None = None) -> bool:
    return is_complete(profile, meta=meta)


def prepare_supplement_draft(
    artifact_path: str | Path,
    *,
    skills_mode: str,
    draft_path: str | Path = "tmp/profile-draft.json",
) -> Path:
    profile = load_artifact(Path(artifact_path))
    meta: dict[str, Any] = {
        "skills_mode": skills_mode,
        "source_artifact": str(artifact_path),
        "skip_resume_link": True,
    }

    if skills_mode == SKILLS_MODE_NEW:
        profile.skills_hard = []
    elif skills_mode == SKILLS_MODE_APPEND:
        meta["collect_skills"] = True
        meta["base_skills"] = [
            {
                "name": skill.name,
                "level": skill.level,
                "provenance": skill.provenance,
            }
            for skill in profile.skills_hard
        ]
        profile.skills_hard = []

    save_draft(draft_path, profile, meta)
    return Path(draft_path)


def prepare_new_draft(
    *,
    skills_mode: str = SKILLS_MODE_NEW,
    draft_path: str | Path = "tmp/profile-draft.json",
) -> Path:
    meta = {"skills_mode": skills_mode}
    profile = ResumeProfile(
        input_mode="questionnaire_only",
        resume_link=None,
    )
    save_draft(draft_path, profile, meta)
    return Path(draft_path)

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from upwork_profile.artifacts import resolve_artifact_path, write_artifact_bundle
from upwork_profile.gaps import completeness_errors, compute_gaps, is_complete
from upwork_profile.models import UpworkProfile
from upwork_profile.schema import FORBIDDEN_ARTIFACT_KEYS
from upwork_profile.writer import finalize_profile, profile_from_dict, profile_to_dict


def load_draft(path: str | Path) -> tuple[UpworkProfile, dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Profile JSON must be an object")

    meta = dict(data.get("_meta") or {})
    profile_data = {key: value for key, value in data.items() if key != "_meta"}
    forbidden = FORBIDDEN_ARTIFACT_KEYS.intersection(profile_data.keys())
    if forbidden:
        raise ValueError(f"Forbidden artifact keys: {', '.join(sorted(forbidden))}")
    return profile_from_dict(profile_data), meta


def save_draft(path: str | Path, profile: UpworkProfile, meta: dict[str, Any] | None = None) -> None:
    payload = profile_to_dict(profile)
    if meta:
        payload["_meta"] = meta
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_profile_json(path: str | Path) -> UpworkProfile:
    profile, _meta = load_draft(path)
    return profile


def merge_extracted_profile(base: UpworkProfile, incoming: UpworkProfile) -> UpworkProfile:
    merged = deepcopy(base)

    if incoming.input_mode:
        merged.input_mode = incoming.input_mode
    if incoming.profile_link:
        merged.profile_link = incoming.profile_link
    if incoming.profile_title.strip():
        merged.profile_title = incoming.profile_title
    if incoming.overview.strip():
        merged.overview = incoming.overview
    if incoming.hourly_rate:
        merged.hourly_rate = incoming.hourly_rate
    if incoming.skills:
        merged.skills = incoming.skills
    if incoming.work_experience_status.strip():
        merged.work_experience_status = incoming.work_experience_status
    if incoming.work_experience:
        merged.work_experience = incoming.work_experience
    if incoming.education:
        merged.education = incoming.education
    if incoming.portfolio_links:
        merged.portfolio_links = incoming.portfolio_links
    if incoming.limitations:
        merged.limitations = incoming.limitations

    merged.sources = incoming.sources
    return merged


def write_profile_artifact(
    profile: UpworkProfile,
    output_path: str | Path | None = None,
    *,
    meta: dict[str, Any] | None = None,
) -> Path:
    finalized = finalize_profile(profile)
    errors = completeness_errors(finalized, meta=meta)
    if errors:
        raise ValueError("; ".join(errors))

    path = Path(output_path) if output_path else resolve_artifact_path(finalized.profile_title)
    return write_artifact_bundle(finalized, path)


def list_gaps(profile: UpworkProfile, meta: dict[str, Any] | None = None) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for gap in compute_gaps(profile, meta=meta):
        items.append(
            {
                "field_id": gap.field_id,
                "question": gap.question,
                "required": gap.required,
            }
        )
    return items


def profile_is_complete(profile: UpworkProfile, meta: dict[str, Any] | None = None) -> bool:
    return is_complete(profile, meta=meta)


def prepare_new_draft(
    draft_path: str | Path = "tmp/upwork-profile-draft.json",
) -> Path:
    profile = UpworkProfile(
        input_mode="questionnaire_only",
        profile_link=None,
    )
    save_draft(draft_path, profile, {})
    return Path(draft_path)

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from resume_profile.models import ResumeProfile, SkillEntry
from resume_profile.schema import FORBIDDEN_ARTIFACT_KEYS
from resume_profile.writer import profile_from_dict, profile_to_dict

SKILLS_MODE_NEW = "new"
SKILLS_MODE_APPEND = "append"


def load_draft(path: str | Path) -> tuple[ResumeProfile, dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Profile JSON must be an object")

    meta = dict(data.get("_meta") or {})
    profile_data = {key: value for key, value in data.items() if key != "_meta"}
    forbidden = FORBIDDEN_ARTIFACT_KEYS.intersection(profile_data.keys())
    if forbidden:
        raise ValueError(f"Forbidden artifact keys: {', '.join(sorted(forbidden))}")
    return profile_from_dict(profile_data), meta


def save_draft(path: str | Path, profile: ResumeProfile, meta: dict[str, Any] | None = None) -> None:
    payload = profile_to_dict(profile)
    if meta:
        payload["_meta"] = meta
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def merge_skill_entries(
    existing: list[SkillEntry],
    incoming: list[SkillEntry],
    *,
    mode: str,
) -> list[SkillEntry]:
    if mode == SKILLS_MODE_NEW:
        return list(incoming)

    merged = list(existing)
    seen = {skill.name.strip().lower() for skill in merged if skill.name.strip()}
    for skill in incoming:
        key = skill.name.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        merged.append(skill)
    return merged

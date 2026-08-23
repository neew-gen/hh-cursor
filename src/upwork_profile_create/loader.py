from __future__ import annotations

import json
import re
from pathlib import Path

from resume_profile.yaml_io import parse_artifact_yaml

from upwork_profile_create.models import (
    CREATE_ENTRY_URL,
    IntelligenceBrief,
    SourceStats,
    UpworkProfile,
    WorkExperienceEntry,
)

PROFILE_ARTIFACTS_DIR = Path("artifacts/upwork-profile")
INTELLIGENCE_DEFAULT_PATH = Path("artifacts/upwork-intelligence.md")
HIGH_CONFIDENCE_PATTERN = re.compile(r"^- \[(high|medium)\]\s*(.+)$", re.IGNORECASE)
SOURCE_ID_PATTERN = re.compile(r"`([^`]+)`")
GENERATED_AT_PATTERN = re.compile(r"_Generated at:\s*(.+?)_")


def list_profiles() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    if not PROFILE_ARTIFACTS_DIR.is_dir():
        return entries

    for yaml_path in sorted(PROFILE_ARTIFACTS_DIR.glob("*.yaml")):
        entries.append(
            {
                "slug": yaml_path.stem,
                "yaml_path": str(yaml_path),
                "profile_title": _profile_title_from_yaml(yaml_path) or yaml_path.stem,
            }
        )
    return entries


def load_profile(path: str | Path) -> UpworkProfile:
    profile_path = Path(path)
    if not profile_path.is_file():
        raise ValueError(f"Cannot load profile {profile_path}: file not found.")

    if profile_path.suffix == ".json":
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    else:
        data = parse_artifact_yaml(profile_path.read_text(encoding="utf-8"))
    return profile_from_dict(data)



def _normalize_hourly_rate(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def profile_from_dict(data: dict) -> UpworkProfile:
    work_experience = [
        WorkExperienceEntry(
            company=item.get("company", ""),
            position=item.get("position", ""),
            start_date=item.get("start_date", ""),
            end_date=item.get("end_date"),
            is_current=bool(item.get("is_current", False)),
            description=item.get("description", ""),
            provenance=item.get("provenance", "from_user_answer"),
        )
        for item in data.get("work_experience") or []
    ]

    sources_data = data.get("sources") or {}
    sources = SourceStats(
        profile_link_used=bool(sources_data.get("profile_link_used", False)),
        fields_from_link=int(sources_data.get("fields_from_link", 0)),
        fields_from_user=int(sources_data.get("fields_from_user", 0)),
    )

    skills_raw = data.get("skills") or []
    if isinstance(skills_raw, dict):
        skills = [item.get("name", "") for item in skills_raw.get("tags") or []]
    else:
        skills = [str(item) for item in skills_raw]

    return UpworkProfile(
        collected_at=data.get("collected_at", ""),
        input_mode=data.get("input_mode", "questionnaire_only"),
        profile_link=data.get("profile_link"),
        profile_title=data.get("profile_title", ""),
        overview=data.get("overview"),
        hourly_rate=_normalize_hourly_rate(data.get("hourly_rate")),
        work_experience=work_experience,
        skills=skills,
        portfolio_links=list(data.get("portfolio_links") or []),
        limitations=list(data.get("limitations") or []),
        sources=sources,
    )


def profile_to_dict(profile: UpworkProfile) -> dict:
    return {
        "collected_at": profile.collected_at,
        "input_mode": profile.input_mode,
        "profile_link": profile.profile_link,
        "profile_title": profile.profile_title,
        "overview": profile.overview,
        "hourly_rate": profile.hourly_rate,
        "work_experience": [
            {
                "company": entry.company,
                "position": entry.position,
                "start_date": entry.start_date,
                "end_date": entry.end_date,
                "is_current": entry.is_current,
                "description": entry.description,
                "provenance": entry.provenance,
            }
            for entry in profile.work_experience
        ],
        "skills": list(profile.skills),
        "portfolio_links": list(profile.portfolio_links),
        "limitations": list(profile.limitations),
        "sources": {
            "profile_link_used": profile.sources.profile_link_used,
            "fields_from_link": profile.sources.fields_from_link,
            "fields_from_user": profile.sources.fields_from_user,
        },
    }


def load_intelligence(path: str | Path | None = None) -> IntelligenceBrief:
    intel_path = Path(path) if path else INTELLIGENCE_DEFAULT_PATH
    if not intel_path.is_file():
        return IntelligenceBrief()

    text = intel_path.read_text(encoding="utf-8")
    generated_match = GENERATED_AT_PATTERN.search(text)
    generated_at = generated_match.group(1).strip() if generated_match else None

    what_to_write = _extract_section_bullets(text, "WhatToWriteInProposals")
    if not what_to_write:
        what_to_write = _extract_section_bullets(text, "WhatToWrite")
    how_to_build = _extract_section_bullets(text, "HowToBuildProfile")
    limitations = _extract_section_bullets(text, "FreshnessAndLimitations")
    source_ids = _extract_source_ids(text)

    return IntelligenceBrief(
        generated_at=generated_at,
        what_to_write=what_to_write,
        how_to_build_profile=how_to_build,
        limitations=limitations,
        source_ids=source_ids,
    )


def resolve_target_url(fill_mode: str, profile_link: str | None) -> str:
    if fill_mode == "edit_existing" and profile_link:
        return profile_link
    return CREATE_ENTRY_URL


def load_inputs(profile_path: str | Path, intelligence_path: str | Path | None = None) -> dict:
    profile = load_profile(profile_path)
    intelligence = load_intelligence(intelligence_path)
    return {
        "profile_path": str(profile_path),
        "profile_title": profile.profile_title,
        "profile_link": profile.profile_link,
        "intelligence_available": bool(
            intelligence.what_to_write or intelligence.how_to_build_profile
        ),
        "intelligence_freshness": intelligence.generated_at,
        "what_to_write": intelligence.what_to_write,
        "how_to_build_profile": intelligence.how_to_build_profile,
        "limitations": intelligence.limitations,
        "intelligence_citations": intelligence.source_ids,
    }


def _profile_title_from_yaml(path: Path) -> str:
    if not path.is_file():
        return ""
    match = re.search(r"^profile_title:\s*(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return ""
    text = match.group(1).strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return text


def _extract_section_bullets(text: str, section_name: str) -> list[str]:
    pattern = re.compile(
        rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return []

    bullets: list[str] = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        bullet_match = HIGH_CONFIDENCE_PATTERN.match(line)
        if bullet_match:
            bullets.append(bullet_match.group(2).strip())
        elif line.startswith("- [") and "]" in line:
            continue
        else:
            bullets.append(line[2:].strip())
    return bullets


def _extract_source_ids(text: str) -> list[str]:
    sources_match = re.search(r"## Sources\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not sources_match:
        return []

    ids: list[str] = []
    for line in sources_match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        id_match = SOURCE_ID_PATTERN.search(line)
        if id_match:
            ids.append(id_match.group(1))
    return ids

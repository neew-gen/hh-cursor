from __future__ import annotations

import re
from pathlib import Path

from resume_profile.artifacts import list_artifact_entries, load_artifact

from resume_create.models import CREATE_ENTRY_URL, IntelligenceBrief

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/resume-intelligence.md")
HIGH_CONFIDENCE_PATTERN = re.compile(r"^- \[(high|medium)\]\s*(.+)$", re.IGNORECASE)
SOURCE_ID_PATTERN = re.compile(r"`([^`]+)`")
GENERATED_AT_PATTERN = re.compile(r"_Generated at:\s*(.+?)_")


def list_profiles() -> list[dict[str, str]]:
    return list_artifact_entries()


def load_profile(path: str | Path):
    return load_artifact(Path(path))


def load_intelligence(path: str | Path | None = None) -> IntelligenceBrief:
    intel_path = Path(path) if path else INTELLIGENCE_DEFAULT_PATH
    if not intel_path.is_file():
        return IntelligenceBrief()

    text = intel_path.read_text(encoding="utf-8")
    generated_match = GENERATED_AT_PATTERN.search(text)
    generated_at = generated_match.group(1).strip() if generated_match else None

    what_to_write = _extract_section_bullets(text, "WhatToWrite")
    how_to_build = _extract_section_bullets(text, "HowToBuildResume")
    limitations = _extract_section_bullets(text, "FreshnessAndLimitations")
    source_ids = _extract_source_ids(text)

    return IntelligenceBrief(
        generated_at=generated_at,
        what_to_write=what_to_write,
        how_to_build_resume=how_to_build,
        limitations=limitations,
        source_ids=source_ids,
    )


def resolve_target_url(fill_mode: str, resume_link: str | None) -> str:
    if fill_mode == "edit_existing" and resume_link:
        return resume_link
    return CREATE_ENTRY_URL


def load_inputs(profile_path: str | Path, intelligence_path: str | Path | None = None) -> dict:
    profile = load_profile(profile_path)
    intelligence = load_intelligence(intelligence_path)
    return {
        "profile_path": str(profile_path),
        "target_role": profile.target_role,
        "resume_link": profile.resume_link,
        "intelligence_available": bool(
            intelligence.what_to_write or intelligence.how_to_build_resume
        ),
        "intelligence_freshness": intelligence.generated_at,
        "what_to_write": intelligence.what_to_write,
        "how_to_build_resume": intelligence.how_to_build_resume,
        "limitations": intelligence.limitations,
        "intelligence_citations": intelligence.source_ids,
    }


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

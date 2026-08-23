from __future__ import annotations

import json
import re
from pathlib import Path

from upwork_profile.artifacts import load_artifact
from upwork_profile.slug import slugify_profile_title

from upwork_proposal.models import JobSnapshot

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/upwork-intelligence.md")
UPWORK_PROFILES_DIR = Path("artifacts/upwork-profile")
HIGH_CONFIDENCE_PATTERN = re.compile(r"^- \[(high|medium)\]\s*(.+)$", re.IGNORECASE)
SOURCE_ID_PATTERN = re.compile(r"`([^`]+)`")
GENERATED_AT_PATTERN = re.compile(r"_Generated at:\s*(.+?)_")


def list_profiles() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    if not UPWORK_PROFILES_DIR.is_dir():
        return entries

    seen_slugs: set[str] = set()
    for yaml_path in sorted(UPWORK_PROFILES_DIR.glob("*.yaml")):
        slug = yaml_path.stem
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        entries.append(
            {
                "slug": slug,
                "yaml_path": str(yaml_path),
                "profile_title": _profile_title_from_yaml(yaml_path) or slug,
            }
        )
    return entries


def load_profile(path: str | Path):
    return load_artifact(Path(path))


def load_job_extract(path: str | Path) -> JobSnapshot:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return JobSnapshot(
        url=str(data.get("url", "")),
        title=str(data.get("title", "")),
        client=str(data.get("client", "")),
        description=str(data.get("description", "")),
        budget_type=str(data.get("budget_type", "")),
        key_skills=[str(item) for item in data.get("key_skills") or []],
        screening_questions=[str(item) for item in data.get("screening_questions") or []],
        extracted_at=str(data.get("extracted_at", "")),
    )


def load_intelligence(path: str | Path | None = None) -> "IntelligenceBrief":
    intel_path = Path(path) if path else INTELLIGENCE_DEFAULT_PATH
    if not intel_path.is_file():
        return IntelligenceBrief()

    text = intel_path.read_text(encoding="utf-8")
    generated_match = GENERATED_AT_PATTERN.search(text)
    generated_at = generated_match.group(1).strip() if generated_match else None

    return IntelligenceBrief(
        generated_at=generated_at,
        what_to_write=_extract_section_bullets(text, "WhatToWriteInProposals"),
        how_to_build_profile=_extract_section_bullets(text, "HowToBuildProfile"),
        limitations=_extract_section_bullets(text, "FreshnessAndLimitations"),
        source_ids=_extract_source_ids(text),
    )


def load_inputs(
    profile_path: str | Path,
    job_path: str | Path | None = None,
    intelligence_path: str | Path | None = None,
) -> dict:
    profile = load_profile(profile_path)
    intelligence = load_intelligence(intelligence_path)
    job_data = None
    if job_path and Path(job_path).is_file():
        snapshot = load_job_extract(job_path)
        job_data = {
            "url": snapshot.url,
            "title": snapshot.title,
            "client": snapshot.client,
            "description": snapshot.description,
            "budget_type": snapshot.budget_type,
            "key_skills": snapshot.key_skills,
            "screening_questions": snapshot.screening_questions,
        }

    return {
        "profile_path": str(profile_path),
        "profile_title": profile.profile_title,
        "profile_link": profile.profile_link,
        "job": job_data,
        "intelligence_available": bool(
            intelligence.what_to_write or intelligence.how_to_build_profile
        ),
        "intelligence_freshness": intelligence.generated_at,
        "what_to_write": intelligence.what_to_write,
        "how_to_build_profile": intelligence.how_to_build_profile,
        "limitations": intelligence.limitations,
        "intelligence_citations": intelligence.source_ids,
    }


class IntelligenceBrief:
    def __init__(
        self,
        generated_at: str | None = None,
        what_to_write: list[str] | None = None,
        how_to_build_profile: list[str] | None = None,
        limitations: list[str] | None = None,
        source_ids: list[str] | None = None,
    ) -> None:
        self.generated_at = generated_at
        self.what_to_write = what_to_write or []
        self.how_to_build_profile = how_to_build_profile or []
        self.limitations = limitations or []
        self.source_ids = source_ids or []


def _profile_title_from_yaml(path: Path) -> str:
    if not path.is_file():
        return ""
    match = re.search(r"^profile_title:\s*(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return ""
    return _strip_yaml_scalar(match.group(1))


def _strip_yaml_scalar(value: str) -> str:
    text = value.strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return text


def profile_slug_from_title(profile_title: str) -> str:
    return slugify_profile_title(profile_title)


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

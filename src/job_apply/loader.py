from __future__ import annotations

import json
from pathlib import Path

from resume_create.loader import load_intelligence
from resume_profile.artifacts import list_artifact_entries, load_artifact

from job_apply.models import VacancySnapshot

INTELLIGENCE_DEFAULT_PATH = Path("artifacts/resume-intelligence.md")


def list_profiles() -> list[dict[str, str]]:
    return list_artifact_entries()


def load_profile(path: str | Path):
    return load_artifact(Path(path))


def load_vacancy_extract(path: str | Path) -> VacancySnapshot:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return VacancySnapshot(
        url=str(data.get("url", "")),
        title=str(data.get("title", "")),
        company=str(data.get("company", "")),
        requirements=[str(item) for item in data.get("requirements") or []],
        key_skills=[str(item) for item in data.get("key_skills") or []],
        extracted_at=str(data.get("extracted_at", "")),
    )


def load_inputs(
    profile_path: str | Path,
    vacancy_path: str | Path | None = None,
    intelligence_path: str | Path | None = None,
) -> dict:
    profile = load_profile(profile_path)
    intelligence = load_intelligence(intelligence_path)
    vacancy_data = None
    if vacancy_path and Path(vacancy_path).is_file():
        snapshot = load_vacancy_extract(vacancy_path)
        vacancy_data = {
            "url": snapshot.url,
            "title": snapshot.title,
            "company": snapshot.company,
            "requirements": snapshot.requirements,
            "key_skills": snapshot.key_skills,
        }

    return {
        "profile_path": str(profile_path),
        "target_role": profile.target_role,
        "resume_link": profile.resume_link,
        "vacancy": vacancy_data,
        "intelligence_available": bool(
            intelligence.what_to_write or intelligence.how_to_build_resume
        ),
        "intelligence_freshness": intelligence.generated_at,
        "what_to_write": intelligence.what_to_write,
        "how_to_build_resume": intelligence.how_to_build_resume,
        "limitations": intelligence.limitations,
        "intelligence_citations": intelligence.source_ids,
    }

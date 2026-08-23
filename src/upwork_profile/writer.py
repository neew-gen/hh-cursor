from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from freelancer_core.models import EducationEntry, WorkExperienceEntry
from upwork_profile.models import UpworkProfile, UpworkSourceStats


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if "\n" in text:
        return "|\n" + "\n".join(f"  {line}" for line in text.splitlines())
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    if any(ch in text for ch in ":{}[],&*#?|-<>=!%@`"):
        return f'"{escaped}"'
    return escaped


def _indent_block(lines: list[str], level: int = 0) -> list[str]:
    prefix = "  " * level
    return [f"{prefix}{line}" for line in lines]


def profile_to_dict(profile: UpworkProfile) -> dict[str, Any]:
    return {
        "collected_at": profile.collected_at,
        "input_mode": profile.input_mode,
        "profile_link": profile.profile_link,
        "profile_title": profile.profile_title,
        "overview": profile.overview,
        "hourly_rate": profile.hourly_rate,
        "skills": profile.skills,
        "work_experience_status": profile.work_experience_status,
        "work_experience": [
            {
                "company": entry.company,
                "position": entry.position,
                "start_date": entry.start_date,
                "end_date": entry.end_date,
                "is_current": entry.is_current,
                "description": entry.description,
                "company_description": entry.company_description,
                "provenance": entry.provenance,
            }
            for entry in profile.work_experience
        ],
        "education": [
            {
                "institution": entry.institution,
                "degree": entry.degree,
                "specialty": entry.specialty,
                "graduation_year": entry.graduation_year,
                "provenance": entry.provenance,
            }
            for entry in profile.education
        ],
        "portfolio_links": profile.portfolio_links,
        "limitations": profile.limitations,
        "sources": {
            "profile_link_used": profile.sources.profile_link_used,
            "fields_from_link": profile.sources.fields_from_link,
            "fields_from_user": profile.sources.fields_from_user,
        },
    }


def render_yaml(profile: UpworkProfile) -> str:
    data = profile_to_dict(profile)
    lines: list[str] = []

    lines.append(f"collected_at: {_yaml_scalar(data['collected_at'])}")
    lines.append(f"input_mode: {_yaml_scalar(data['input_mode'])}")
    lines.append(f"profile_link: {_yaml_scalar(data['profile_link'])}")
    lines.append(f"profile_title: {_yaml_scalar(data['profile_title'])}")
    overview = data["overview"]
    if "\n" in overview:
        lines.append("overview: |")
        lines.extend(_indent_block(overview.splitlines(), 1))
    else:
        lines.append(f"overview: {_yaml_scalar(overview)}")
    lines.append(f"hourly_rate: {_yaml_scalar(data['hourly_rate'])}")

    lines.append("skills:")
    for item in data["skills"]:
        lines.extend(_indent_block([f"- {_yaml_scalar(item)}"], 0))

    lines.append(f"work_experience_status: {_yaml_scalar(data['work_experience_status'])}")
    lines.append("work_experience:")
    for entry in data["work_experience"]:
        lines.append("  - company: " + _yaml_scalar(entry["company"]))
        lines.append("    position: " + _yaml_scalar(entry["position"]))
        lines.append("    start_date: " + _yaml_scalar(entry["start_date"]))
        lines.append("    end_date: " + _yaml_scalar(entry["end_date"]))
        lines.append("    is_current: " + _yaml_scalar(entry["is_current"]))
        desc = entry["description"]
        if "\n" in desc:
            lines.append("    description: |")
            lines.extend(_indent_block(desc.splitlines(), 3))
        else:
            lines.append("    description: " + _yaml_scalar(desc))
        if entry.get("company_description"):
            lines.append(
                "    company_description: "
                + _yaml_scalar(entry["company_description"])
            )
        lines.append("    provenance: " + _yaml_scalar(entry["provenance"]))

    lines.append("education:")
    for entry in data["education"]:
        lines.append("  - institution: " + _yaml_scalar(entry["institution"]))
        lines.append("    degree: " + _yaml_scalar(entry["degree"]))
        lines.append("    specialty: " + _yaml_scalar(entry["specialty"]))
        lines.append(
            "    graduation_year: " + _yaml_scalar(entry["graduation_year"])
        )
        lines.append("    provenance: " + _yaml_scalar(entry["provenance"]))

    lines.append("portfolio_links:")
    for item in data["portfolio_links"]:
        lines.extend(_indent_block([f"- {_yaml_scalar(item)}"], 0))

    lines.append("limitations:")
    for item in data["limitations"]:
        lines.extend(_indent_block([f"- {_yaml_scalar(item)}"], 0))

    lines.append("sources:")
    lines.append(
        "  profile_link_used: "
        + _yaml_scalar(data["sources"]["profile_link_used"])
    )
    lines.append(
        "  fields_from_link: "
        + _yaml_scalar(data["sources"]["fields_from_link"])
    )
    lines.append(
        "  fields_from_user: "
        + _yaml_scalar(data["sources"]["fields_from_user"])
    )

    return "\n".join(lines) + "\n"


def profile_from_dict(data: dict[str, Any]) -> UpworkProfile:
    work_experience = [
        WorkExperienceEntry(
            company=item.get("company", ""),
            position=item.get("position", ""),
            start_date=item.get("start_date", ""),
            end_date=item.get("end_date"),
            is_current=bool(item.get("is_current", False)),
            description=item.get("description", ""),
            company_description=item.get("company_description"),
            provenance=item.get("provenance", "from_user_answer"),
        )
        for item in data.get("work_experience") or []
    ]

    education = [
        EducationEntry(
            institution=item.get("institution", ""),
            degree=item.get("degree", ""),
            specialty=item.get("specialty", ""),
            graduation_year=item.get("graduation_year"),
            provenance=item.get("provenance", "from_user_answer"),
        )
        for item in data.get("education") or []
    ]

    sources_data = data.get("sources") or {}
    sources = UpworkSourceStats(
        profile_link_used=bool(sources_data.get("profile_link_used", False)),
        fields_from_link=int(sources_data.get("fields_from_link", 0)),
        fields_from_user=int(sources_data.get("fields_from_user", 0)),
    )

    return UpworkProfile(
        collected_at=data.get("collected_at", ""),
        input_mode=data.get("input_mode", "questionnaire_only"),
        profile_link=data.get("profile_link"),
        profile_title=data.get("profile_title", ""),
        overview=data.get("overview", ""),
        hourly_rate=data.get("hourly_rate"),
        skills=list(data.get("skills") or []),
        work_experience_status=data.get("work_experience_status", ""),
        work_experience=work_experience,
        education=education,
        portfolio_links=list(data.get("portfolio_links") or []),
        limitations=list(data.get("limitations") or []),
        sources=sources,
    )


def finalize_profile(profile: UpworkProfile) -> UpworkProfile:
    if not profile.collected_at:
        profile.collected_at = datetime.now(timezone.utc).isoformat()

    user_fields = 0
    link_fields = 0
    for entry in profile.work_experience:
        if entry.provenance == "from_resume_link":
            link_fields += 1
        else:
            user_fields += 1
    for entry in profile.education:
        if entry.provenance == "from_resume_link":
            link_fields += 1
        else:
            user_fields += 1
    if profile.profile_title and profile.sources.fields_from_link == 0:
        user_fields += 1
    if profile.overview.strip():
        user_fields += 1
    if profile.hourly_rate:
        user_fields += 1
    if profile.skills:
        user_fields += 1

    profile.sources.fields_from_link = link_fields
    profile.sources.fields_from_user = user_fields
    profile.sources.profile_link_used = profile.input_mode == "questionnaire_with_link"
    return profile

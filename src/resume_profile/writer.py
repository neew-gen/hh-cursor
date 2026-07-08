from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from resume_profile.models import (
    EducationEntry,
    LanguageEntry,
    ResumeProfile,
    SkillEntry,
    SourceStats,
    WorkExperienceEntry,
    WorkPreferences,
)


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


def profile_to_dict(profile: ResumeProfile) -> dict[str, Any]:
    return {
        "collected_at": profile.collected_at,
        "input_mode": profile.input_mode,
        "resume_link": profile.resume_link,
        "target_role": profile.target_role,
        "specializations": profile.specializations,
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
        "skills": {
            "hard": [
                {
                    "name": skill.name,
                    "level": skill.level,
                    "provenance": skill.provenance,
                }
                for skill in profile.skills_hard
            ],
            "soft": [
                {
                    "name": skill.name,
                    "level": skill.level,
                    "provenance": skill.provenance,
                }
                for skill in profile.skills_soft
            ],
        },
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
        "no_formal_education": profile.no_formal_education,
        "about_me": profile.about_me,
        "work_preferences": _work_preferences_to_dict(profile.work_preferences),
        "languages": [
            {"name": lang.name, "level": lang.level} for lang in profile.languages
        ],
        "additional_education": profile.additional_education,
        "portfolio_links": profile.portfolio_links,
        "personal_links": profile.personal_links,
        "limitations": profile.limitations,
        "sources": {
            "resume_link_used": profile.sources.resume_link_used,
            "fields_from_link": profile.sources.fields_from_link,
            "fields_from_user": profile.sources.fields_from_user,
        },
    }


def _work_preferences_to_dict(prefs: WorkPreferences | None) -> dict[str, Any] | None:
    if prefs is None:
        return None
    return {
        "salary": prefs.salary,
        "employment_type": prefs.employment_type,
        "work_format": prefs.work_format,
        "commute_time": prefs.commute_time,
        "business_trips": prefs.business_trips,
    }


def render_yaml(profile: ResumeProfile) -> str:
    data = profile_to_dict(profile)
    lines: list[str] = []

    lines.append(f"collected_at: {_yaml_scalar(data['collected_at'])}")
    lines.append(f"input_mode: {_yaml_scalar(data['input_mode'])}")
    lines.append(f"resume_link: {_yaml_scalar(data['resume_link'])}")
    lines.append(f"target_role: {_yaml_scalar(data['target_role'])}")
    lines.append("specializations:")
    for item in data["specializations"]:
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

    lines.append("skills:")
    lines.append("  hard:")
    for skill in data["skills"]["hard"]:
        lines.append("    - name: " + _yaml_scalar(skill["name"]))
        lines.append("      level: " + _yaml_scalar(skill["level"]))
        lines.append("      provenance: " + _yaml_scalar(skill["provenance"]))
    lines.append("  soft:")
    for skill in data["skills"]["soft"]:
        lines.append("    - name: " + _yaml_scalar(skill["name"]))
        lines.append("      level: " + _yaml_scalar(skill["level"]))
        lines.append("      provenance: " + _yaml_scalar(skill["provenance"]))

    lines.append("education:")
    for entry in data["education"]:
        lines.append("  - institution: " + _yaml_scalar(entry["institution"]))
        lines.append("    degree: " + _yaml_scalar(entry["degree"]))
        lines.append("    specialty: " + _yaml_scalar(entry["specialty"]))
        lines.append(
            "    graduation_year: " + _yaml_scalar(entry["graduation_year"])
        )
        lines.append("    provenance: " + _yaml_scalar(entry["provenance"]))

    lines.append(f"no_formal_education: {_yaml_scalar(data['no_formal_education'])}")
    lines.append(f"about_me: {_yaml_scalar(data['about_me'])}")

    lines.append("work_preferences:")
    prefs = data["work_preferences"]
    if prefs is None:
        lines.append("  null")
    else:
        for key, value in prefs.items():
            lines.append(f"  {key}: {_yaml_scalar(value)}")

    lines.append("languages:")
    for lang in data["languages"]:
        lines.append("  - name: " + _yaml_scalar(lang["name"]))
        lines.append("    level: " + _yaml_scalar(lang["level"]))

    for list_key in ("additional_education", "portfolio_links", "personal_links"):
        lines.append(f"{list_key}:")
        for item in data[list_key]:
            lines.extend(_indent_block([f"- {_yaml_scalar(item)}"], 0))

    lines.append("limitations:")
    for item in data["limitations"]:
        lines.extend(_indent_block([f"- {_yaml_scalar(item)}"], 0))

    lines.append("sources:")
    lines.append(
        "  resume_link_used: "
        + _yaml_scalar(data["sources"]["resume_link_used"])
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


def profile_from_dict(data: dict[str, Any]) -> ResumeProfile:
    skills = data.get("skills") or {}
    hard = [
        SkillEntry(
            name=item.get("name", ""),
            level=item.get("level", "medium"),
            provenance=item.get("provenance", "from_user_answer"),
        )
        for item in skills.get("hard") or []
    ]
    soft = [
        SkillEntry(
            name=item.get("name", ""),
            level=item.get("level", "medium"),
            provenance=item.get("provenance", "from_user_answer"),
        )
        for item in skills.get("soft") or []
    ]

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

    prefs_data = data.get("work_preferences")
    work_preferences = None
    if isinstance(prefs_data, dict):
        work_preferences = WorkPreferences(
            salary=prefs_data.get("salary"),
            employment_type=prefs_data.get("employment_type"),
            work_format=prefs_data.get("work_format"),
            commute_time=prefs_data.get("commute_time"),
            business_trips=prefs_data.get("business_trips"),
        )

    sources_data = data.get("sources") or {}
    sources = SourceStats(
        resume_link_used=bool(sources_data.get("resume_link_used", False)),
        fields_from_link=int(sources_data.get("fields_from_link", 0)),
        fields_from_user=int(sources_data.get("fields_from_user", 0)),
    )

    languages = [
        LanguageEntry(name=item.get("name", ""), level=item.get("level", ""))
        for item in data.get("languages") or []
    ]

    return ResumeProfile(
        collected_at=data.get("collected_at", ""),
        input_mode=data.get("input_mode", "questionnaire_only"),
        resume_link=data.get("resume_link"),
        target_role=data.get("target_role", ""),
        specializations=list(data.get("specializations") or []),
        work_experience_status=data.get("work_experience_status", ""),
        work_experience=work_experience,
        skills_hard=hard,
        skills_soft=soft,
        education=education,
        no_formal_education=bool(data.get("no_formal_education", False)),
        about_me=data.get("about_me"),
        work_preferences=work_preferences,
        languages=languages,
        additional_education=list(data.get("additional_education") or []),
        portfolio_links=list(data.get("portfolio_links") or []),
        personal_links=list(data.get("personal_links") or []),
        limitations=list(data.get("limitations") or []),
        sources=sources,
    )


def finalize_profile(profile: ResumeProfile) -> ResumeProfile:
    if not profile.collected_at:
        profile.collected_at = datetime.now(timezone.utc).isoformat()

    user_fields = 0
    link_fields = 0
    for skill in profile.skills_hard + profile.skills_soft:
        if skill.provenance == "from_resume_link":
            link_fields += 1
        else:
            user_fields += 1
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
    if profile.target_role and profile.sources.fields_from_link == 0:
        user_fields += 1

    profile.sources.fields_from_link = link_fields
    profile.sources.fields_from_user = user_fields
    profile.sources.resume_link_used = profile.input_mode == "questionnaire_with_link"
    return profile

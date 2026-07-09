from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from job_apply.models import ApplicationPlan, ApplicationReport, CoverLetter, SectionStatus, VacancySnapshot
from resume_profile.yaml_io import parse_artifact_yaml


def application_plan_to_dict(plan: ApplicationPlan) -> dict[str, Any]:
    return {
        "composed_at": plan.composed_at,
        "vacancy": {
            "url": plan.vacancy.url,
            "title": plan.vacancy.title,
            "company": plan.vacancy.company,
            "requirements": list(plan.vacancy.requirements),
            "key_skills": list(plan.vacancy.key_skills),
            "extracted_at": plan.vacancy.extracted_at,
        },
        "source_profile": plan.source_profile,
        "target_role": plan.target_role,
        "resume_match_hint": plan.resume_match_hint,
        "cover_letter": {
            "text": plan.cover_letter.text,
            "language": plan.cover_letter.language,
            "char_count": plan.cover_letter.char_count,
        },
        "rewrite_applied": plan.rewrite_applied,
        "intelligence_path": plan.intelligence_path,
        "intelligence_freshness": plan.intelligence_freshness,
        "intelligence_citations": list(plan.intelligence_citations),
        "limitations": list(plan.limitations),
    }


def render_application_plan_yaml(plan: ApplicationPlan) -> str:
    lines = [
        f"composed_at: {_yaml_scalar(plan.composed_at)}",
        "vacancy:",
        f"  url: {_yaml_scalar(plan.vacancy.url)}",
        f"  title: {_yaml_scalar(plan.vacancy.title)}",
        f"  company: {_yaml_scalar(plan.vacancy.company)}",
        "  requirements:",
    ]
    for item in plan.vacancy.requirements:
        lines.append(f"    - {_yaml_scalar(item)}")
    lines.append("  key_skills:")
    for item in plan.vacancy.key_skills:
        lines.append(f"    - {_yaml_scalar(item)}")
    lines.append(f"  extracted_at: {_yaml_scalar(plan.vacancy.extracted_at)}")
    lines.extend(
        [
            f"source_profile: {_yaml_scalar(plan.source_profile)}",
            f"target_role: {_yaml_scalar(plan.target_role)}",
            f"resume_match_hint: {_yaml_scalar(plan.resume_match_hint)}",
            "cover_letter:",
            f"  text: {_yaml_block_scalar(plan.cover_letter.text, indent=4)}",
            f"  language: {_yaml_scalar(plan.cover_letter.language)}",
            f"  char_count: {_yaml_scalar(plan.cover_letter.char_count)}",
            f"rewrite_applied: {_yaml_scalar(plan.rewrite_applied)}",
            f"intelligence_path: {_yaml_scalar(plan.intelligence_path)}",
            f"intelligence_freshness: {_yaml_scalar(plan.intelligence_freshness)}",
            "intelligence_citations:",
        ]
    )
    for citation in plan.intelligence_citations:
        lines.append(f"  - {_yaml_scalar(citation)}")
    lines.append("limitations:")
    for limitation in plan.limitations:
        lines.append(f"  - {_yaml_scalar(limitation)}")
    return "\n".join(lines) + "\n"


def load_application_plan(path: str | Path) -> ApplicationPlan:
    data = parse_artifact_yaml(Path(path).read_text(encoding="utf-8"))
    vacancy_data = data.get("vacancy") or {}
    cover_data = data.get("cover_letter") or {}
    return ApplicationPlan(
        composed_at=data.get("composed_at", ""),
        vacancy=VacancySnapshot(
            url=vacancy_data.get("url", ""),
            title=vacancy_data.get("title", ""),
            company=vacancy_data.get("company", ""),
            requirements=list(vacancy_data.get("requirements") or []),
            key_skills=list(vacancy_data.get("key_skills") or []),
            extracted_at=vacancy_data.get("extracted_at", ""),
        ),
        source_profile=data.get("source_profile", ""),
        target_role=data.get("target_role", ""),
        resume_match_hint=data.get("resume_match_hint", ""),
        cover_letter=CoverLetter(
            text=cover_data.get("text", ""),
            language=cover_data.get("language", "ru"),
            char_count=int(cover_data.get("char_count") or 0),
        ),
        rewrite_applied=bool(data.get("rewrite_applied", False)),
        intelligence_path=data.get("intelligence_path"),
        intelligence_freshness=data.get("intelligence_freshness"),
        intelligence_citations=list(data.get("intelligence_citations") or []),
        limitations=list(data.get("limitations") or []),
    )


def write_application_plan(plan: ApplicationPlan, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_application_plan_yaml(plan), encoding="utf-8")
    return str(path)


def render_application_report_yaml(report: ApplicationReport) -> str:
    lines = [
        f"reported_at: {_yaml_scalar(report.reported_at)}",
        f"application_plan_path: {_yaml_scalar(report.application_plan_path)}",
        f"submitted: {_yaml_scalar(report.submitted)}",
        "blockers:",
    ]
    for blocker in report.blockers:
        lines.append(f"  - {_yaml_scalar(blocker)}")
    lines.append("sections:")
    for section in report.sections:
        lines.append(f"  - section_id: {_yaml_scalar(section.section_id)}")
        lines.append(f"    status: {_yaml_scalar(section.status)}")
        lines.append(f"    notes: {_yaml_scalar(section.notes)}")
    return "\n".join(lines) + "\n"


def write_application_report(report: ApplicationReport, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_application_report_yaml(report), encoding="utf-8")
    return str(path)


def build_application_report(
    application_plan_path: str,
    sections: list[dict[str, str]],
    blockers: list[str] | None = None,
) -> ApplicationReport:
    return ApplicationReport(
        reported_at=datetime.now(timezone.utc).isoformat(),
        application_plan_path=application_plan_path,
        submitted=False,
        sections=[
            SectionStatus(
                section_id=item.get("section_id", ""),
                status=item.get("status", "skipped"),
                notes=item.get("notes", ""),
            )
            for item in sections
        ],
        blockers=list(blockers or []),
    )


def _yaml_block_scalar(text: str, indent: int = 2) -> str:
    prefix = " " * indent
    return "|\n" + "\n".join(f"{prefix}{line}" for line in text.splitlines())


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
        return _yaml_block_scalar(text, indent=2)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    if any(ch in text for ch in ":{}[],&*#?|-<>=!%@`"):
        return f'"{escaped}"'
    return escaped

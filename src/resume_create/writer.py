from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resume_profile.writer import profile_from_dict, profile_to_dict, render_yaml
from resume_profile.yaml_io import parse_artifact_yaml

from resume_create.models import FillPlan, FillPlanMeta, FillReport, RewriteApplied, SectionStatus


def fill_plan_to_dict(fill_plan: FillPlan) -> dict[str, Any]:
    data = profile_to_dict(fill_plan.profile)
    meta = fill_plan.meta
    data["composed_at"] = meta.composed_at
    data["source_profile"] = meta.source_profile
    data["intelligence_path"] = meta.intelligence_path
    data["intelligence_freshness"] = meta.intelligence_freshness
    data["fill_mode"] = meta.fill_mode
    data["target_url"] = meta.target_url
    data["rewrite_applied"] = {
        "about_me": meta.rewrite_applied.about_me,
        "work_experience_descriptions": meta.rewrite_applied.work_experience_descriptions,
    }
    data["intelligence_citations"] = meta.intelligence_citations
    return data


def render_fill_plan_yaml(fill_plan: FillPlan) -> str:
    profile_yaml = render_yaml(fill_plan.profile).rstrip("\n")
    meta_lines = [
        f"composed_at: {_yaml_scalar(fill_plan.meta.composed_at)}",
        f"source_profile: {_yaml_scalar(fill_plan.meta.source_profile)}",
        f"intelligence_path: {_yaml_scalar(fill_plan.meta.intelligence_path)}",
        f"intelligence_freshness: {_yaml_scalar(fill_plan.meta.intelligence_freshness)}",
        f"fill_mode: {_yaml_scalar(fill_plan.meta.fill_mode)}",
        f"target_url: {_yaml_scalar(fill_plan.meta.target_url)}",
        "rewrite_applied:",
        f"  about_me: {_yaml_scalar(fill_plan.meta.rewrite_applied.about_me)}",
        "  work_experience_descriptions: "
        + _yaml_scalar(fill_plan.meta.rewrite_applied.work_experience_descriptions),
        "intelligence_citations:",
    ]
    for citation in fill_plan.meta.intelligence_citations:
        meta_lines.append(f"  - {_yaml_scalar(citation)}")

    return "\n".join(meta_lines) + "\n" + profile_yaml + "\n"


def load_fill_plan(path: str) -> FillPlan:
    data = parse_artifact_yaml(Path(path).read_text(encoding="utf-8"))
    meta = FillPlanMeta(
        composed_at=data.get("composed_at", ""),
        source_profile=data.get("source_profile", ""),
        intelligence_path=data.get("intelligence_path"),
        intelligence_freshness=data.get("intelligence_freshness"),
        fill_mode=data.get("fill_mode", "create_new"),
        target_url=data.get("target_url", ""),
        rewrite_applied=_rewrite_from_dict(data.get("rewrite_applied") or {}),
        intelligence_citations=list(data.get("intelligence_citations") or []),
    )
    profile = profile_from_dict(data)
    return FillPlan(profile=profile, meta=meta)


def write_fill_plan(fill_plan: FillPlan, output_path: str) -> str:
    content = render_fill_plan_yaml(fill_plan)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return output_path


def render_fill_report_yaml(report: FillReport) -> str:
    lines = [
        f"reported_at: {_yaml_scalar(report.reported_at)}",
        f"fill_plan_path: {_yaml_scalar(report.fill_plan_path)}",
        f"fill_mode: {_yaml_scalar(report.fill_mode)}",
        f"published: {_yaml_scalar(report.published)}",
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


def write_fill_report(report: FillReport, output_path: str) -> str:
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(render_fill_report_yaml(report))
    return output_path


def _rewrite_from_dict(data: dict[str, Any]) -> RewriteApplied:
    return RewriteApplied(
        about_me=bool(data.get("about_me", False)),
        work_experience_descriptions=bool(
            data.get("work_experience_descriptions", False)
        ),
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


def build_fill_report(
    fill_plan_path: str,
    fill_mode: str,
    sections: list[dict[str, str]],
    blockers: list[str] | None = None,
) -> FillReport:
    return FillReport(
        reported_at=datetime.now(timezone.utc).isoformat(),
        fill_plan_path=fill_plan_path,
        fill_mode=fill_mode,
        sections=[
            SectionStatus(
                section_id=item.get("section_id", ""),
                status=item.get("status", "skipped"),
                notes=item.get("notes", ""),
            )
            for item in sections
        ],
        blockers=list(blockers or []),
        published=False,
    )

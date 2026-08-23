from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resume_profile.yaml_io import parse_artifact_yaml

from upwork_profile_create.models import FillPlan, FillPlanMeta, FillReport, RewriteApplied, SectionStatus
from upwork_profile_create.loader import profile_from_dict, profile_to_dict


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
        "overview": meta.rewrite_applied.overview,
        "profile_title": meta.rewrite_applied.profile_title,
        "work_experience_descriptions": meta.rewrite_applied.work_experience_descriptions,
        "skills_tags": meta.rewrite_applied.skills_tags,
    }
    data["intelligence_citations"] = meta.intelligence_citations
    return data


def render_fill_plan_yaml(fill_plan: FillPlan) -> str:
    profile_yaml = _render_profile_yaml(fill_plan.profile).rstrip("\n")
    meta_lines = [
        f"composed_at: {_yaml_scalar(fill_plan.meta.composed_at)}",
        f"source_profile: {_yaml_scalar(fill_plan.meta.source_profile)}",
        f"intelligence_path: {_yaml_scalar(fill_plan.meta.intelligence_path)}",
        f"intelligence_freshness: {_yaml_scalar(fill_plan.meta.intelligence_freshness)}",
        f"fill_mode: {_yaml_scalar(fill_plan.meta.fill_mode)}",
        f"target_url: {_yaml_scalar(fill_plan.meta.target_url)}",
        "rewrite_applied:",
        f"  overview: {_yaml_scalar(fill_plan.meta.rewrite_applied.overview)}",
        f"  profile_title: {_yaml_scalar(fill_plan.meta.rewrite_applied.profile_title)}",
        "  work_experience_descriptions: "
        + _yaml_scalar(fill_plan.meta.rewrite_applied.work_experience_descriptions),
        f"  skills_tags: {_yaml_scalar(fill_plan.meta.rewrite_applied.skills_tags)}",
        "intelligence_citations:",
    ]
    for citation in fill_plan.meta.intelligence_citations:
        meta_lines.append(f"  - {_yaml_scalar(citation)}")

    return "\n".join(meta_lines) + "\n" + profile_yaml + "\n"


def _render_profile_yaml(profile) -> str:
    data = profile_to_dict(profile)
    lines: list[str] = []
    lines.append(f"collected_at: {_yaml_scalar(data['collected_at'])}")
    lines.append(f"input_mode: {_yaml_scalar(data['input_mode'])}")
    lines.append(f"profile_link: {_yaml_scalar(data['profile_link'])}")
    lines.append(f"profile_title: {_yaml_scalar(data['profile_title'])}")
    lines.append(f"overview: {_yaml_scalar(data['overview'])}")
    lines.append(f"hourly_rate: {_yaml_scalar(data.get('hourly_rate'))}")
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
            lines.extend(f"      {line}" for line in desc.splitlines())
        else:
            lines.append("    description: " + _yaml_scalar(desc))
        lines.append("    provenance: " + _yaml_scalar(entry["provenance"]))
    lines.append("skills:")
    for skill in data["skills"]:
        lines.append(f"  - {_yaml_scalar(skill)}")
    lines.append("portfolio_links:")
    for link in data["portfolio_links"]:
        lines.append(f"  - {_yaml_scalar(link)}")
    lines.append("limitations:")
    for item in data["limitations"]:
        lines.append(f"  - {_yaml_scalar(item)}")
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


def load_fill_plan(path: str | Path) -> FillPlan:
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
        overview=bool(data.get("overview", False)),
        profile_title=bool(data.get("profile_title", False)),
        work_experience_descriptions=bool(
            data.get("work_experience_descriptions", False)
        ),
        skills_tags=bool(data.get("skills_tags", False)),
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

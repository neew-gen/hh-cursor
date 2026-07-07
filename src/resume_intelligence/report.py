from __future__ import annotations

from .models import RecommendationItem, ResumeIntelligenceReport


def _render_recommendations(items: list[RecommendationItem]) -> list[str]:
    if not items:
        return ["- No recommendations available."]

    lines: list[str] = []
    for item in items:
        sources = ", ".join(f"`{source}`" for source in item.supporting_sources) or "`no-source`"
        line = (
            f"- [{item.confidence}] {item.recommendation_text} "
            f"(sources: {sources}; rationale: {item.rationale})"
        )
        if item.conflict_note:
            line += f" Conflict: {item.conflict_note}"
        lines.append(line)
    return lines


def render_markdown(report: ResumeIntelligenceReport) -> str:
    generated_at = report.generated_at.isoformat() if report.generated_at else "unknown"
    sections: list[str] = [
        "# Resume Intelligence",
        "",
        f"_Generated at: {generated_at}_",
        "",
        "## Summary",
    ]

    sections.extend(f"- {point}" for point in report.summary_points)
    sections.extend(
        [
            "",
            "## HowHRAndATSProcessResumesNow",
            *_render_recommendations(report.screening_findings),
            "",
            "## WhatToWrite",
            *_render_recommendations(report.content_recommendations),
            "",
            "## HowToBuildResume",
            *_render_recommendations(report.format_recommendations),
            "",
            "## SourceQualityAndConflicts",
        ]
    )

    if report.conflicts:
        sections.extend(f"- {item}" for item in report.conflicts)
    else:
        sections.append("- No major cross-source conflicts were detected in this run.")

    sections.extend(["", "## Sources"])
    sections.extend(f"- {item}" for item in report.source_notes)

    sections.extend(["", "## FreshnessAndLimitations"])
    sections.extend(f"- {item}" for item in report.limitations)

    return "\n".join(sections).strip() + "\n"

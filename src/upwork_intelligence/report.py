from __future__ import annotations

from .models import RecommendationItem, UpworkIntelligenceReport


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


def render_markdown(report: UpworkIntelligenceReport) -> str:
    generated_at = report.generated_at.isoformat() if report.generated_at else "unknown"
    sections: list[str] = [
        "# Upwork Intelligence",
        "",
        f"_Generated at: {generated_at}_",
        "",
        "## Summary",
    ]

    sections.extend(f"- {point}" for point in report.summary_points)
    sections.extend(
        [
            "",
            "## HowClientsReviewProposalsNow",
            *_render_recommendations(report.proposal_review_findings),
            "",
            "## WhatToWriteInProposals",
            *_render_recommendations(report.proposal_recommendations),
            "",
            "## HowToBuildProfile",
            *_render_recommendations(report.profile_recommendations),
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

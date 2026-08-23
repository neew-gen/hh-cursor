from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from project_portfolio_extract.models import PortfolioArtifact, PortfolioDraft, ProjectFacts


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


def render_portfolio_yaml(artifact: PortfolioArtifact) -> str:
    data = artifact.to_dict()
    lines: list[str] = []
    for key in (
        "parsed_at",
        "project_slug",
        "title",
        "description",
        "project_url",
        "skills",
        "source_type",
        "repo_url",
        "local_path",
        "last_commit_date",
        "last_commit_sha",
        "stack",
        "readme_excerpt",
        "approved_by_user",
        "limitations",
    ):
        value = data.get(key)
        if key in {"skills", "stack", "limitations"}:
            lines.append(f"{key}:")
            for item in value or []:
                lines.append(f"  - {_yaml_scalar(item)}")
            continue
        lines.append(f"{key}: {_yaml_scalar(value)}")
    return "\n".join(lines) + "\n"


def build_artifact(
    project_slug: str,
    facts: ProjectFacts,
    draft: PortfolioDraft,
    *,
    approved_by_user: bool = True,
    limitations: list[str] | None = None,
) -> PortfolioArtifact:
    parsed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return PortfolioArtifact(
        parsed_at=parsed_at,
        project_slug=project_slug,
        title=draft.title,
        description=draft.description,
        project_url=draft.project_url,
        skills=draft.skills,
        source_type=facts.source_type,
        repo_url=facts.repo_url,
        local_path=facts.local_path,
        last_commit_date=facts.last_commit_date,
        last_commit_sha=facts.last_commit_sha,
        stack=facts.stack,
        readme_excerpt=facts.readme_excerpt,
        approved_by_user=approved_by_user,
        limitations=limitations or [],
    )

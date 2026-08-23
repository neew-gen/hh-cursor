from __future__ import annotations

from project_portfolio_extract.models import PortfolioDraft, ProjectFacts


def compose_portfolio(facts: ProjectFacts) -> PortfolioDraft:
    title = _compose_title(facts.name)
    project_url = facts.repo_url or ""
    skills = _compose_skills(facts)
    description = _compose_description(facts, skills)
    return PortfolioDraft(
        title=title,
        description=description,
        project_url=project_url,
        skills=skills,
    )


def _compose_title(name: str) -> str:
    text = name.strip()
    if len(text) <= 70:
        return text
    return text[:67].rstrip() + "..."


def _compose_skills(facts: ProjectFacts) -> list[str]:
    skills: list[str] = []
    seen: set[str] = set()
    for item in facts.stack:
        if item not in seen:
            seen.add(item)
            skills.append(item)
    for item in facts.languages_hint:
        if item not in seen:
            seen.add(item)
            skills.append(item)
    return skills[:10]


def _compose_description(facts: ProjectFacts, skills: list[str]) -> str:
    intro = facts.summary.strip() or facts.readme_excerpt.strip() or facts.name
    lines = [intro.rstrip(".") + "."]
    if skills:
        lines.append(f"Stack: {', '.join(skills[:6])}.")
    if facts.readme_excerpt and facts.readme_excerpt not in intro:
        extra = facts.readme_excerpt.strip()
        if extra and extra not in intro:
            lines.append(extra.rstrip(".") + ".")
    return "\n".join(lines[:3])

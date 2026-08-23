from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProjectFacts:
    name: str
    summary: str
    readme_excerpt: str
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)
    stack: list[str] = field(default_factory=list)
    languages_hint: list[str] = field(default_factory=list)
    last_commit_date: str | None = None
    last_commit_sha: str | None = None
    repo_url: str | None = None
    local_path: str = ""
    source_type: str = "local_path"
    stale: bool = False
    stale_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "name": self.name,
            "summary": self.summary,
            "readme_excerpt": self.readme_excerpt,
            "dependencies": self.dependencies,
            "dev_dependencies": self.dev_dependencies,
            "stack": self.stack,
            "languages_hint": self.languages_hint,
            "last_commit_date": self.last_commit_date,
            "last_commit_sha": self.last_commit_sha,
            "repo_url": self.repo_url,
            "local_path": self.local_path,
            "source_type": self.source_type,
        }
        if self.stale:
            data["stale"] = True
            data["stale_reason"] = self.stale_reason
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectFacts:
        return cls(
            name=str(data.get("name") or ""),
            summary=str(data.get("summary") or ""),
            readme_excerpt=str(data.get("readme_excerpt") or ""),
            dependencies=list(data.get("dependencies") or []),
            dev_dependencies=list(data.get("dev_dependencies") or []),
            stack=list(data.get("stack") or []),
            languages_hint=list(data.get("languages_hint") or []),
            last_commit_date=data.get("last_commit_date"),
            last_commit_sha=data.get("last_commit_sha"),
            repo_url=data.get("repo_url"),
            local_path=str(data.get("local_path") or ""),
            source_type=str(data.get("source_type") or "local_path"),
            stale=bool(data.get("stale")),
            stale_reason=data.get("stale_reason"),
        )


@dataclass
class PortfolioDraft:
    title: str
    description: str
    project_url: str
    skills: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "project_url": self.project_url,
            "skills": self.skills,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PortfolioDraft:
        return cls(
            title=str(data.get("title") or ""),
            description=str(data.get("description") or ""),
            project_url=str(data.get("project_url") or ""),
            skills=list(data.get("skills") or []),
        )


@dataclass
class PortfolioArtifact:
    parsed_at: str
    project_slug: str
    title: str
    description: str
    project_url: str
    skills: list[str]
    source_type: str
    repo_url: str | None = None
    local_path: str = ""
    last_commit_date: str | None = None
    last_commit_sha: str | None = None
    stack: list[str] = field(default_factory=list)
    readme_excerpt: str = ""
    approved_by_user: bool = True
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "parsed_at": self.parsed_at,
            "project_slug": self.project_slug,
            "title": self.title,
            "description": self.description,
            "project_url": self.project_url,
            "skills": self.skills,
            "source_type": self.source_type,
            "repo_url": self.repo_url,
            "local_path": self.local_path,
            "last_commit_date": self.last_commit_date,
            "last_commit_sha": self.last_commit_sha,
            "stack": self.stack,
            "readme_excerpt": self.readme_excerpt,
            "approved_by_user": self.approved_by_user,
            "limitations": self.limitations,
        }

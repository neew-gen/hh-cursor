from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from resume_profile.slug import slugify_target_role

ARTIFACTS_DIR = Path("artifacts/project-portfolio-extract")
GITHUB_CLONES_DIR = Path("tmp/github-clones")
PROJECT_UNPACKS_DIR = Path("tmp/project-unpacks")


def slugify_project_name(name: str) -> str:
    return slugify_target_role(name)


def parse_github_url(url: str) -> tuple[str, str, str] | None:
    parsed = urlparse(url.strip().rstrip("/"))
    if parsed.netloc not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    canonical = f"https://github.com/{owner}/{repo}"
    return owner, repo, canonical


def clone_target_path(owner: str, repo: str) -> Path:
    return GITHUB_CLONES_DIR / f"{owner}-{repo}"


def artifact_path(project_slug: str) -> Path:
    return ARTIFACTS_DIR / f"{project_slug}.yaml"


def resolve_artifact_path(project_slug: str) -> Path:
    base = artifact_path(project_slug)
    if not base.exists():
        return base
    stem = base.stem
    suffix = base.suffix
    index = 2
    while True:
        candidate = base.with_name(f"{stem} ({index}){suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def slug_from_github_url(url: str) -> str:
    parsed = parse_github_url(url)
    if not parsed:
        return slugify_project_name(url)
    _, repo, _ = parsed
    return slugify_project_name(repo)


def normalize_repo_url(url: str | None) -> str | None:
    if not url:
        return None
    parsed = parse_github_url(url)
    if parsed:
        return parsed[2]
    return url.strip()

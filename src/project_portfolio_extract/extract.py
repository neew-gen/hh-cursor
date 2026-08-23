from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from project_portfolio_extract.models import ProjectFacts

README_NAMES = ("README.md", "readme.md", "Readme.md", "README.MD")

DEPENDENCY_SKILL_MAP = {
    "vue": "Vue.js",
    "react": "React",
    "typescript": "TypeScript",
    "nestjs": "NestJS",
    "nuxt": "Nuxt.js",
    "express": "Node.js",
    "node": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "redis": "Redis",
    "docker": "Docker",
    "vitest": "Vitest",
    "jest": "JavaScript",
    "webpack": "webpack",
    "vite": "Vite",
    "tailwindcss": "Tailwind CSS",
    "sass": "Sass",
    "scss": "Sass",
    "firebase": "Firebase",
    "prisma": "Prisma",
    "rabbitmq": "RabbitMQ",
}

EXTENSION_LANGUAGE_MAP = {
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".vue": "Vue.js",
    ".py": "Python",
    ".go": "Go",
    ".rs": "Rust",
}


def extract_facts(
    root: Path,
    *,
    repo_url: str | None = None,
    source_type: str = "local_path",
) -> ProjectFacts:
    root = root.resolve()
    readme_path = _find_readme(root)
    readme_text = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path else ""
    name = _readme_title(readme_text) or _package_name(root) or root.name
    summary = _package_description(root) or _first_sentence(readme_text) or name
    readme_excerpt = _readme_excerpt(readme_text)
    dependencies, dev_dependencies = _read_manifest_deps(root)
    languages_hint = _detect_languages(root)
    stack = _build_stack(dependencies, dev_dependencies, languages_hint)
    last_commit_date, last_commit_sha = _git_head(root)
    stale, stale_reason = _stale_flags(last_commit_date)

    return ProjectFacts(
        name=name,
        summary=summary,
        readme_excerpt=readme_excerpt,
        dependencies=dependencies,
        dev_dependencies=dev_dependencies,
        stack=stack,
        languages_hint=languages_hint,
        last_commit_date=last_commit_date,
        last_commit_sha=last_commit_sha,
        repo_url=repo_url,
        local_path=str(root),
        source_type=source_type,
        stale=stale,
        stale_reason=stale_reason,
    )


def _find_readme(root: Path) -> Path | None:
    for name in README_NAMES:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def _readme_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def _readme_excerpt(text: str) -> str:
    lines: list[str] = []
    past_title = False
    for line in text.splitlines():
        stripped = line.strip()
        if not past_title:
            if stripped.startswith("# "):
                past_title = True
            continue
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("#"):
            break
        if stripped.startswith("[!") or stripped.startswith("![") or stripped.startswith("<img"):
            continue
        lines.append(stripped)
        if len(" ".join(lines)) > 400:
            break
    return " ".join(lines)


def _first_sentence(text: str) -> str:
    excerpt = _readme_excerpt(text) or text.strip()
    if not excerpt:
        return ""
    match = re.split(r"(?<=[.!?])\s+", excerpt, maxsplit=1)
    return match[0].strip()


def _package_name(root: Path) -> str:
    package_json = root / "package.json"
    if package_json.is_file():
        data = json.loads(package_json.read_text(encoding="utf-8"))
        name = str(data.get("name") or "").strip()
        if name.startswith("@"):
            name = name.split("/", 1)[-1]
        return name
    return ""


def _package_description(root: Path) -> str:
    package_json = root / "package.json"
    if package_json.is_file():
        data = json.loads(package_json.read_text(encoding="utf-8"))
        return str(data.get("description") or "").strip()
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        text = pyproject.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'^description\s*=\s*"([^"]+)"', text, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def _read_manifest_deps(root: Path) -> tuple[list[str], list[str]]:
    package_json = root / "package.json"
    if not package_json.is_file():
        return [], []
    data = json.loads(package_json.read_text(encoding="utf-8"))
    deps = sorted(str(key) for key in (data.get("dependencies") or {}).keys())
    dev_deps = sorted(str(key) for key in (data.get("devDependencies") or {}).keys())
    return deps, dev_deps


def _detect_languages(root: Path) -> list[str]:
    counts: dict[str, int] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if "node_modules" in path.parts or "dist" in path.parts:
            continue
        language = EXTENSION_LANGUAGE_MAP.get(path.suffix.lower())
        if language:
            counts[language] = counts.get(language, 0) + 1
        if sum(counts.values()) >= 200:
            break
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [name for name, _ in ordered[:5]]


def _build_stack(
    dependencies: list[str],
    dev_dependencies: list[str],
    languages_hint: list[str],
) -> list[str]:
    seen: set[str] = set()
    stack: list[str] = []
    for dep in dependencies + dev_dependencies:
        key = dep.lower().split("/")[-1]
        label = DEPENDENCY_SKILL_MAP.get(key)
        if label and label not in seen:
            seen.add(label)
            stack.append(label)
    for language in languages_hint:
        if language not in seen:
            seen.add(language)
            stack.append(language)
    return stack[:8]


def _git_head(root: Path) -> tuple[str | None, str | None]:
    git_dir = root / ".git"
    if not git_dir.exists():
        return None, None
    result = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%cI|%h"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None, None
    date_part, _, sha = result.stdout.strip().partition("|")
    date_value = date_part[:10] if date_part else None
    return date_value, sha or None


def _stale_flags(last_commit_date: str | None) -> tuple[bool, str | None]:
    if not last_commit_date:
        return False, None
    try:
        commit_day = datetime.fromisoformat(last_commit_date).date()
    except ValueError:
        return False, None
    threshold = datetime.now(timezone.utc).date() - timedelta(days=730)
    if commit_day < threshold:
        return True, "last commit older than 2 years"
    return False, None

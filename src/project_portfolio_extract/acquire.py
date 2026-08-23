from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path

from project_portfolio_extract.artifacts import (
    GITHUB_CLONES_DIR,
    PROJECT_UNPACKS_DIR,
    clone_target_path,
    parse_github_url,
)


class AcquireError(Exception):
    pass


def ensure_git_available() -> None:
    if shutil.which("git") is None:
        raise AcquireError("git is not available on PATH")


def shallow_clone(url: str) -> Path:
    parsed = parse_github_url(url)
    if not parsed:
        raise AcquireError(f"Not a GitHub URL: {url}")
    owner, repo, canonical = parsed
    target = clone_target_path(owner, repo)
    ensure_git_available()
    GITHUB_CLONES_DIR.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", canonical, str(target)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "clone failed").strip()
        raise AcquireError(message)
    return target


def acquire_from_url(url: str) -> tuple[Path, str]:
    path = shallow_clone(url)
    parsed = parse_github_url(url)
    canonical = parsed[2] if parsed else url
    return path, canonical


def acquire_from_path(path: str) -> Path:
    target = Path(path).expanduser().resolve()
    if not target.is_dir():
        raise AcquireError(f"Local path is not a directory: {path}")
    return target


def unpack_zip(zip_path: str, slug: str) -> Path:
    source = Path(zip_path).expanduser().resolve()
    if not source.is_file():
        raise AcquireError(f"ZIP file not found: {zip_path}")
    PROJECT_UNPACKS_DIR.mkdir(parents=True, exist_ok=True)
    target = PROJECT_UNPACKS_DIR / slugify_unpack_slug(slug)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, "r") as archive:
        archive.extractall(target)
    nested = _single_top_level_dir(target)
    return nested if nested else target


def slugify_unpack_slug(slug: str) -> str:
    from project_portfolio_extract.artifacts import slugify_project_name

    return slugify_project_name(slug)


def _single_top_level_dir(root: Path) -> Path | None:
    entries = [entry for entry in root.iterdir() if not entry.name.startswith(".")]
    if len(entries) == 1 and entries[0].is_dir():
        return entries[0]
    return None

from __future__ import annotations

import json
import re
from pathlib import Path

from resume_profile.models import ResumeProfile
from resume_profile.slug import slugify_target_role
from resume_profile.writer import profile_from_dict, render_yaml
from resume_profile.yaml_io import parse_artifact_yaml

ARTIFACTS_DIR = Path("artifacts/resume-profile")
LEGACY_ARTIFACT_PATH = Path("artifacts/resume-profile.yaml")


def artifact_path(target_role: str) -> Path:
    slug = slugify_target_role(target_role)
    return ARTIFACTS_DIR / f"{slug}.yaml"


def resolve_artifact_path(target_role: str) -> Path:
    base_path = artifact_path(target_role)
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    index = 2
    while True:
        candidate = base_path.with_name(f"{stem} ({index}){suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def has_saved_artifacts() -> bool:
    if LEGACY_ARTIFACT_PATH.is_file():
        return True

    if not ARTIFACTS_DIR.is_dir():
        return False

    return next(ARTIFACTS_DIR.glob("*.yaml"), None) is not None


def list_artifact_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen_slugs: set[str] = set()

    if LEGACY_ARTIFACT_PATH.is_file():
        entries.append(
            {
                "slug": "legacy",
                "yaml_path": str(LEGACY_ARTIFACT_PATH),
                "target_role": _target_role_from_yaml(LEGACY_ARTIFACT_PATH),
            }
        )

    if not ARTIFACTS_DIR.is_dir():
        return entries

    for yaml_path in sorted(ARTIFACTS_DIR.glob("*.yaml")):
        slug = yaml_path.stem
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        entries.append(
            {
                "slug": slug,
                "yaml_path": str(yaml_path),
                "target_role": _target_role_from_yaml(yaml_path) or slug,
            }
        )
    return entries


def write_artifact_bundle(profile: ResumeProfile, yaml_path: Path | None = None) -> Path:
    path = yaml_path or resolve_artifact_path(profile.target_role)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_yaml(profile), encoding="utf-8")
    stale_json = path.with_suffix(".json")
    if stale_json.is_file():
        stale_json.unlink()
    return path


def load_artifact(path: Path) -> ResumeProfile:
    if path.suffix == ".json" and path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        return profile_from_dict(data)

    if not path.is_file():
        raise ValueError(f"Cannot load artifact {path}: file not found.")

    data = parse_artifact_yaml(path.read_text(encoding="utf-8"))
    return profile_from_dict(data)


def _target_role_from_yaml(path: Path) -> str:
    if not path.is_file():
        return ""
    match = re.search(r"^target_role:\s*(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return ""
    return _strip_yaml_scalar(match.group(1))


def _strip_yaml_scalar(value: str) -> str:
    text = value.strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return text

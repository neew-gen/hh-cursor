from __future__ import annotations

import json
import re
from pathlib import Path

from freelancer_core.yaml_io import parse_artifact_yaml
from upwork_profile.models import UpworkProfile
from upwork_profile.slug import slugify_profile_title
from upwork_profile.writer import profile_from_dict, render_yaml

ARTIFACTS_DIR = Path("artifacts/upwork-profile")


def artifact_path(profile_title: str) -> Path:
    slug = slugify_profile_title(profile_title)
    return ARTIFACTS_DIR / f"{slug}.yaml"


def resolve_artifact_path(profile_title: str) -> Path:
    base_path = artifact_path(profile_title)
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


def write_artifact_bundle(profile: UpworkProfile, yaml_path: Path | None = None) -> Path:
    path = yaml_path or resolve_artifact_path(profile.profile_title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_yaml(profile), encoding="utf-8")
    stale_json = path.with_suffix(".json")
    if stale_json.is_file():
        stale_json.unlink()
    return path


def load_artifact(path: Path) -> UpworkProfile:
    if path.suffix == ".json" and path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        return profile_from_dict(data)

    if not path.is_file():
        raise ValueError(f"Cannot load artifact {path}: file not found.")

    data = parse_artifact_yaml(path.read_text(encoding="utf-8"))
    return profile_from_dict(data)


def _profile_title_from_yaml(path: Path) -> str:
    if not path.is_file():
        return ""
    match = re.search(
        r"^profile_title:\s*(.+)$",
        path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        return ""
    return _strip_yaml_scalar(match.group(1))


def _strip_yaml_scalar(value: str) -> str:
    text = value.strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return text

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from upwork_profile.artifacts import resolve_artifact_path
from upwork_profile.extractor import extract_from_page_text, is_valid_upwork_profile_link
from upwork_profile.runner import (
    load_draft,
    list_gaps,
    merge_extracted_profile,
    prepare_new_draft,
    profile_is_complete,
    write_profile_artifact,
)
from upwork_profile.slug import slugify_profile_title
from upwork_profile.writer import profile_to_dict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upwork profile collection CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gaps_parser = subparsers.add_parser("gaps", help="List missing Upwork profile fields.")
    gaps_parser.add_argument("--input", required=True, help="Draft profile JSON path.")

    write_parser = subparsers.add_parser("write", help="Write Upwork profile artifact.")
    write_parser.add_argument("--input", required=True, help="Profile JSON path.")
    write_parser.add_argument(
        "--output",
        default=None,
        help="Output YAML path (default: artifacts/upwork-profile/<profile-title-slug>.yaml).",
    )

    extract_parser = subparsers.add_parser(
        "extract-text",
        help="Extract profile fields from Upwork page text snapshot.",
    )
    extract_parser.add_argument("--input", required=True, help="Page text file path.")
    extract_parser.add_argument("--output", required=True, help="Output JSON path.")
    extract_parser.add_argument("--profile-link", default=None, help="Source Upwork profile URL.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate profile completeness.",
    )
    validate_parser.add_argument("--input", required=True, help="Profile JSON draft.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve artifact path for profile title.",
    )
    artifact_path_parser.add_argument("--profile-title", required=True, help="Profile title.")

    init_parser = subparsers.add_parser(
        "init-draft",
        help="Initialize tmp/upwork-profile-draft.json for a collection session.",
    )
    init_parser.add_argument(
        "--output",
        default="tmp/upwork-profile-draft.json",
        help="Draft JSON output path.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "gaps":
        profile, meta = load_draft(args.input)
        gaps = list_gaps(profile, meta=meta)
        print(json.dumps(gaps, ensure_ascii=False, indent=2))
        return 0

    if args.command == "write":
        profile, meta = load_draft(args.input)
        output = args.output
        if output is None and not profile.profile_title.strip():
            print("profile_title is required to resolve artifact path.", file=sys.stderr)
            return 2
        if output is None:
            output = str(resolve_artifact_path(profile.profile_title))
        path = write_profile_artifact(profile, output, meta=meta)
        print(str(path))
        return 0

    if args.command == "extract-text":
        if args.profile_link and not is_valid_upwork_profile_link(args.profile_link):
            print("Invalid Upwork profile link.", file=sys.stderr)
            return 2
        page_text = Path(args.input).read_text(encoding="utf-8")
        profile = extract_from_page_text(page_text, profile_link=args.profile_link)
        output = Path(args.output)
        meta = None
        if output.is_file():
            try:
                existing_profile, meta = load_draft(output)
            except (ValueError, json.JSONDecodeError, OSError):
                existing_profile = None
            else:
                profile = merge_extracted_profile(existing_profile, profile)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = profile_to_dict(profile)
        if meta:
            payload["_meta"] = meta
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(output))
        return 0

    if args.command == "validate":
        profile, meta = load_draft(args.input)
        complete = profile_is_complete(profile, meta=meta)
        print(
            json.dumps(
                {"complete": complete, "gaps": list_gaps(profile, meta=meta)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if complete else 1

    if args.command == "artifact-path":
        slug = slugify_profile_title(args.profile_title)
        path = resolve_artifact_path(args.profile_title)
        print(json.dumps({"slug": slug, "yaml_path": str(path)}, ensure_ascii=False))
        return 0

    if args.command == "init-draft":
        prepare_new_draft(draft_path=args.output)
        print(args.output)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

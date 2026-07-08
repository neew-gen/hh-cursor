from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from resume_profile.artifacts import (
    has_saved_artifacts,
    list_artifact_entries,
    resolve_artifact_path,
)
from resume_profile.draft import SKILLS_MODE_APPEND, SKILLS_MODE_NEW, load_draft
from resume_profile.extractor import extract_from_page_text, extract_resume_content, is_valid_hh_resume_link
from resume_profile.runner import (
    list_gaps,
    load_profile_json,
    merge_extracted_profile,
    prepare_new_draft,
    prepare_supplement_draft,
    profile_is_complete,
    write_profile_artifact,
)
from resume_profile.slug import slugify_target_role
from resume_profile.writer import profile_to_dict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resume profile collection CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gaps_parser = subparsers.add_parser("gaps", help="List missing required hh fields.")
    gaps_parser.add_argument("--input", required=True, help="Draft profile JSON path.")

    write_parser = subparsers.add_parser("write", help="Write resume profile artifact.")
    write_parser.add_argument("--input", required=True, help="Profile JSON path.")
    write_parser.add_argument(
        "--output",
        default=None,
        help="Output YAML path (default: artifacts/resume-profile/<target-role-slug>.yaml).",
    )

    extract_parser = subparsers.add_parser(
        "extract-text",
        help="Extract profile fields from hh page text snapshot.",
    )
    extract_parser.add_argument("--input", required=True, help="Page text file path.")
    extract_parser.add_argument("--output", required=True, help="Output JSON path.")
    extract_parser.add_argument("--resume-link", default=None, help="Source resume URL.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate profile completeness.",
    )
    validate_parser.add_argument("--input", required=True, help="Profile JSON draft.")

    subparsers.add_parser(
        "has-artifacts",
        help="Check whether any saved resume profile artifacts exist.",
    )

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Check saved artifacts and initialize a new draft when none exist.",
    )
    bootstrap_parser.add_argument(
        "--output",
        default="tmp/profile-draft.json",
        help="Draft JSON output path when initializing a new profile.",
    )

    subparsers.add_parser("list-artifacts", help="List saved resume profile artifacts.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve artifact path for target role.",
    )
    artifact_path_parser.add_argument("--target-role", required=True, help="Target role title.")

    init_parser = subparsers.add_parser(
        "init-draft",
        help="Initialize tmp/profile-draft.json for a collection session.",
    )
    init_parser.add_argument(
        "--skills-mode",
        choices=(SKILLS_MODE_NEW, SKILLS_MODE_APPEND),
        default=SKILLS_MODE_NEW,
        help="Whether skills replace or append to a saved profile.",
    )
    init_parser.add_argument(
        "--from-artifact",
        default=None,
        help="Existing artifact YAML/JSON path for supplement mode.",
    )
    init_parser.add_argument(
        "--output",
        default="tmp/profile-draft.json",
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
        if output is None and not profile.target_role.strip():
            print("target_role is required to resolve artifact path.", file=sys.stderr)
            return 2
        if output is None:
            output = str(resolve_artifact_path(profile.target_role))
        path = write_profile_artifact(profile, output, meta=meta)
        print(str(path))
        return 0

    if args.command == "extract-text":
        if args.resume_link and not is_valid_hh_resume_link(args.resume_link):
            print("Invalid hh.ru resume link.", file=sys.stderr)
            return 2
        page_text = Path(args.input).read_text(encoding="utf-8")
        profile = extract_resume_content(page_text, resume_link=args.resume_link)
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

    if args.command == "has-artifacts":
        print(json.dumps({"has_artifacts": has_saved_artifacts()}, ensure_ascii=False))
        return 0

    if args.command == "bootstrap":
        has_artifacts = has_saved_artifacts()
        result: dict[str, object] = {"has_artifacts": has_artifacts}
        if has_artifacts:
            result["artifacts"] = list_artifact_entries()
        else:
            prepare_new_draft(skills_mode=SKILLS_MODE_NEW, draft_path=args.output)
            result["draft_initialized"] = True
            result["draft_path"] = args.output
            result["skills_mode"] = SKILLS_MODE_NEW
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "list-artifacts":
        print(json.dumps(list_artifact_entries(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "artifact-path":
        slug = slugify_target_role(args.target_role)
        path = resolve_artifact_path(args.target_role)
        print(json.dumps({"slug": slug, "yaml_path": str(path)}, ensure_ascii=False))
        return 0

    if args.command == "init-draft":
        if args.from_artifact:
            prepare_supplement_draft(
                args.from_artifact,
                skills_mode=args.skills_mode,
                draft_path=args.output,
            )
        else:
            prepare_new_draft(skills_mode=args.skills_mode, draft_path=args.output)
        print(args.output)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

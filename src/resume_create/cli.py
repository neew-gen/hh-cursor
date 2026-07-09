from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from resume_create.artifacts import ensure_artifacts_dir, resolve_fill_plan_path, resolve_report_path
from resume_create.composer import compose_fill_plan
from resume_create.loader import list_profiles, load_inputs
from resume_create.mapper import list_form_mappings
from resume_create.validator import validate_fill_plan, validate_fill_plan_file
from resume_create.writer import build_fill_report, write_fill_plan, write_fill_report
from resume_profile.slug import slugify_target_role


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resume create CLI for hh.ru fill-plan.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-profiles", help="List saved resume profile artifacts.")

    load_parser = subparsers.add_parser(
        "load-inputs",
        help="Load profile and intelligence summary.",
    )
    load_parser.add_argument("--profile", required=True, help="Profile YAML path.")
    load_parser.add_argument(
        "--intelligence",
        default=None,
        help="Intelligence MD path (default: artifacts/resume-intelligence.md).",
    )

    compose_parser = subparsers.add_parser(
        "compose",
        help="Compose fill-plan from profile and rewritten draft JSON.",
    )
    compose_parser.add_argument("--profile", required=True, help="Source profile YAML.")
    compose_parser.add_argument("--draft", required=True, help="Draft JSON with rewritten texts.")
    compose_parser.add_argument(
        "--fill-mode",
        choices=("create_new", "edit_existing"),
        required=True,
        help="hh.ru fill mode.",
    )
    compose_parser.add_argument("--intelligence", default=None, help="Intelligence MD path.")
    compose_parser.add_argument("--output", default=None, help="Output fill-plan YAML path.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate fill-plan factual integrity against source profile.",
    )
    validate_parser.add_argument("--input", required=True, help="Fill-plan YAML path.")
    validate_parser.add_argument("--profile", required=True, help="Source profile YAML path.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve fill-plan artifact path for target role.",
    )
    artifact_path_parser.add_argument("--target-role", required=True, help="Target role title.")

    subparsers.add_parser("form-mappings", help="List hh.ru form field mappings.")

    report_parser = subparsers.add_parser(
        "write-report",
        help="Write browser fill report YAML.",
    )
    report_parser.add_argument("--fill-plan", required=True, help="Fill-plan YAML path.")
    report_parser.add_argument(
        "--sections",
        required=True,
        help="JSON file with section statuses.",
    )
    report_parser.add_argument("--blockers", default=None, help="JSON array of blocker strings.")
    report_parser.add_argument("--output", default=None, help="Report output path.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-profiles":
        print(json.dumps(list_profiles(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "load-inputs":
        result = load_inputs(args.profile, args.intelligence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "compose":
        fill_plan = compose_fill_plan(
            profile_path=args.profile,
            draft_path=args.draft,
            fill_mode=args.fill_mode,
            intelligence_path=args.intelligence,
        )
        errors = validate_fill_plan(fill_plan, args.profile)
        if errors:
            print(json.dumps({"errors": errors}, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1

        ensure_artifacts_dir()
        output = args.output
        if output is None:
            output = str(resolve_fill_plan_path(fill_plan.profile.target_role))
        path = write_fill_plan(fill_plan, output)
        print(path)
        return 0

    if args.command == "validate":
        errors = validate_fill_plan_file(args.input, args.profile)
        payload = {"valid": not errors, "errors": errors}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    if args.command == "artifact-path":
        slug = slugify_target_role(args.target_role)
        path = resolve_fill_plan_path(args.target_role)
        print(json.dumps({"slug": slug, "yaml_path": str(path)}, ensure_ascii=False))
        return 0

    if args.command == "form-mappings":
        print(json.dumps(list_form_mappings(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "write-report":
        fill_plan_path = Path(args.fill_plan)
        sections = json.loads(Path(args.sections).read_text(encoding="utf-8"))
        blockers = None
        if args.blockers:
            blockers = json.loads(Path(args.blockers).read_text(encoding="utf-8"))

        from resume_create.writer import load_fill_plan

        fill_plan = load_fill_plan(str(fill_plan_path))
        report = build_fill_report(
            fill_plan_path=str(fill_plan_path),
            fill_mode=fill_plan.meta.fill_mode,
            sections=sections,
            blockers=blockers,
        )
        output = args.output
        if output is None:
            output = str(resolve_report_path(fill_plan.profile.target_role))
        path = write_fill_report(report, output)
        print(path)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from job_apply.artifacts import ensure_artifacts_dir, resolve_application_plan_path, resolve_report_path
from job_apply.composer import compose_application_plan
from job_apply.loader import list_profiles, load_inputs
from job_apply.slug import vacancy_slug_from_snapshot
from job_apply.validator import validate_application_plan, validate_application_plan_file
from job_apply.writer import (
    build_application_report,
    write_application_plan,
    write_application_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Job apply CLI for hh.ru application plans.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-profiles", help="List saved resume profile artifacts.")

    load_parser = subparsers.add_parser(
        "load-inputs",
        help="Load profile, vacancy extract, and intelligence summary.",
    )
    load_parser.add_argument("--profile", required=True, help="Profile YAML path.")
    load_parser.add_argument("--vacancy", default=None, help="Vacancy extract JSON path.")
    load_parser.add_argument(
        "--intelligence",
        default=None,
        help="Intelligence MD path (default: artifacts/resume-intelligence.md).",
    )

    compose_parser = subparsers.add_parser(
        "compose",
        help="Compose application plan from profile, vacancy extract, and cover letter draft.",
    )
    compose_parser.add_argument("--profile", required=True, help="Source profile YAML.")
    compose_parser.add_argument("--vacancy", required=True, help="Vacancy extract JSON.")
    compose_parser.add_argument("--draft", required=True, help="Cover letter draft JSON.")
    compose_parser.add_argument("--intelligence", default=None, help="Intelligence MD path.")
    compose_parser.add_argument("--output", default=None, help="Output application plan path.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate application plan factual integrity.",
    )
    validate_parser.add_argument("--input", required=True, help="Application plan YAML path.")
    validate_parser.add_argument("--profile", required=True, help="Source profile YAML path.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve application plan artifact path for vacancy.",
    )
    artifact_path_parser.add_argument("--vacancy-url", required=True, help="Vacancy URL.")
    artifact_path_parser.add_argument("--company", default="", help="Vacancy company name.")
    artifact_path_parser.add_argument("--title", default="", help="Vacancy title.")

    report_parser = subparsers.add_parser(
        "write-report",
        help="Write browser apply report YAML.",
    )
    report_parser.add_argument(
        "--application-plan",
        required=True,
        help="Application plan YAML path.",
    )
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
        profiles = list_profiles()
        print(json.dumps(profiles, ensure_ascii=False, indent=2))
        return 0

    if args.command == "load-inputs":
        result = load_inputs(args.profile, args.vacancy, args.intelligence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "compose":
        plan = compose_application_plan(
            profile_path=args.profile,
            vacancy_path=args.vacancy,
            draft_path=args.draft,
            intelligence_path=args.intelligence,
        )
        slug = vacancy_slug_from_snapshot(
            plan.vacancy.url,
            plan.vacancy.company,
            plan.vacancy.title,
        )
        ensure_artifacts_dir()
        output = args.output or str(resolve_application_plan_path(slug))
        write_application_plan(plan, output)
        print(output)
        return 0

    if args.command == "validate":
        errors = validate_application_plan_file(args.input, args.profile)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("OK")
        return 0

    if args.command == "artifact-path":
        slug = vacancy_slug_from_snapshot(args.vacancy_url, args.company, args.title)
        print(resolve_application_plan_path(slug))
        return 0

    if args.command == "write-report":
        sections = json.loads(Path(args.sections).read_text(encoding="utf-8"))
        blockers = None
        if args.blockers:
            blockers = json.loads(Path(args.blockers).read_text(encoding="utf-8"))
        plan_path = Path(args.application_plan)
        slug = plan_path.stem
        report = build_application_report(
            application_plan_path=str(plan_path),
            sections=sections,
            blockers=blockers,
        )
        output = args.output or str(resolve_report_path(slug))
        write_application_report(report, output)
        print(output)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

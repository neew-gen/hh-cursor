from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from upwork_proposal.artifacts import ensure_artifacts_dir, resolve_proposal_plan_path, resolve_report_path
from upwork_proposal.composer import compose_proposal_plan
from upwork_proposal.loader import list_profiles, load_inputs
from upwork_proposal.slug import job_slug_from_snapshot
from upwork_proposal.validator import validate_proposal_plan, validate_proposal_plan_file
from upwork_proposal.writer import (
    build_proposal_report,
    write_proposal_plan,
    write_proposal_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upwork proposal CLI for proposal plans.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-profiles", help="List saved upwork profile artifacts.")

    load_parser = subparsers.add_parser(
        "load-inputs",
        help="Load profile, job extract, and intelligence summary.",
    )
    load_parser.add_argument("--profile", required=True, help="Profile YAML path.")
    load_parser.add_argument("--job", default=None, help="Job extract JSON path.")
    load_parser.add_argument(
        "--intelligence",
        default=None,
        help="Intelligence MD path (default: artifacts/upwork-intelligence.md).",
    )

    compose_parser = subparsers.add_parser(
        "compose",
        help="Compose proposal plan from profile, job extract, and proposal draft.",
    )
    compose_parser.add_argument("--profile", required=True, help="Source profile YAML.")
    compose_parser.add_argument("--job", required=True, help="Job extract JSON.")
    compose_parser.add_argument("--draft", required=True, help="Proposal draft JSON.")
    compose_parser.add_argument("--intelligence", default=None, help="Intelligence MD path.")
    compose_parser.add_argument("--output", default=None, help="Output proposal plan path.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate proposal plan factual integrity.",
    )
    validate_parser.add_argument("--input", required=True, help="Proposal plan YAML path.")
    validate_parser.add_argument("--profile", required=True, help="Source profile YAML path.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve proposal plan artifact path for job.",
    )
    artifact_path_parser.add_argument("--job-url", required=True, help="Upwork job URL.")
    artifact_path_parser.add_argument("--client", default="", help="Job client name.")
    artifact_path_parser.add_argument("--title", default="", help="Job title.")

    report_parser = subparsers.add_parser(
        "write-report",
        help="Write browser proposal report YAML.",
    )
    report_parser.add_argument(
        "--proposal-plan",
        required=True,
        help="Proposal plan YAML path.",
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
        result = load_inputs(args.profile, args.job, args.intelligence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "compose":
        plan = compose_proposal_plan(
            profile_path=args.profile,
            job_path=args.job,
            draft_path=args.draft,
            intelligence_path=args.intelligence,
        )
        slug = job_slug_from_snapshot(
            plan.job.url,
            plan.job.client,
            plan.job.title,
        )
        ensure_artifacts_dir()
        output = args.output or str(resolve_proposal_plan_path(slug))
        write_proposal_plan(plan, output)
        print(output)
        return 0

    if args.command == "validate":
        errors = validate_proposal_plan_file(args.input, args.profile)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("OK")
        return 0

    if args.command == "artifact-path":
        slug = job_slug_from_snapshot(args.job_url, args.client, args.title)
        print(resolve_proposal_plan_path(slug))
        return 0

    if args.command == "write-report":
        sections = json.loads(Path(args.sections).read_text(encoding="utf-8"))
        blockers = None
        if args.blockers:
            blockers = json.loads(Path(args.blockers).read_text(encoding="utf-8"))
        plan_path = Path(args.proposal_plan)
        slug = plan_path.stem
        report = build_proposal_report(
            proposal_plan_path=str(plan_path),
            sections=sections,
            blockers=blockers,
        )
        output = args.output or str(resolve_report_path(slug))
        write_proposal_report(report, output)
        print(output)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

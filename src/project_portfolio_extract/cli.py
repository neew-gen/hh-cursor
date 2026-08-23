from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from project_portfolio_extract.acquire import (
    AcquireError,
    acquire_from_path,
    acquire_from_url,
    unpack_zip,
)
from project_portfolio_extract.artifacts import (
    artifact_path,
    resolve_artifact_path,
)
from project_portfolio_extract.compose import compose_portfolio
from project_portfolio_extract.extract import extract_facts
from project_portfolio_extract.models import PortfolioDraft, ProjectFacts
from project_portfolio_extract.writer import build_artifact, render_portfolio_yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract portfolio-ready project descriptions.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_url = subparsers.add_parser(
        "extract-from-url",
        help="Shallow clone GitHub URL and extract project facts.",
    )
    extract_url.add_argument("--url", required=True, help="Public GitHub repository URL.")
    extract_url.add_argument("--output", default=None, help="Write facts JSON to path.")

    extract_path = subparsers.add_parser(
        "extract-from-path",
        help="Extract project facts from a local directory.",
    )
    extract_path.add_argument("--path", required=True, help="Local project directory.")
    extract_path.add_argument("--repo-url", default=None, help="Canonical repo URL.")
    extract_path.add_argument(
        "--source-type",
        choices=("local_path", "zip_upload", "github_url"),
        default="local_path",
        help="Source type label for facts.",
    )
    extract_path.add_argument("--output", default=None, help="Write facts JSON to path.")

    unpack_parser = subparsers.add_parser("unpack", help="Unpack ZIP to gitignored temp dir.")
    unpack_parser.add_argument("--zip", required=True, help="Path to ZIP archive.")
    unpack_parser.add_argument("--slug", required=True, help="Slug for unpack directory.")

    compose_parser = subparsers.add_parser(
        "compose-portfolio",
        help="Compose portfolio draft from facts JSON.",
    )
    compose_parser.add_argument("--facts", required=True, help="Facts JSON path.")
    compose_parser.add_argument("--output", default=None, help="Write portfolio draft JSON.")

    write_parser = subparsers.add_parser(
        "write-artifact",
        help="Write portfolio artifact YAML from facts + draft JSON.",
    )
    write_parser.add_argument("--facts", required=True, help="Facts JSON path.")
    write_parser.add_argument("--draft", required=True, help="Portfolio draft JSON path.")
    write_parser.add_argument("--project-slug", required=True, help="Artifact slug.")
    write_parser.add_argument(
        "--approved-by-user",
        choices=("true", "false"),
        default="true",
        help="Whether user approved this project.",
    )
    write_parser.add_argument("--output", default=None, help="Output YAML path.")

    artifact_path_parser = subparsers.add_parser(
        "artifact-path",
        help="Resolve artifact path for project slug.",
    )
    artifact_path_parser.add_argument("--project-slug", required=True, help="Project slug.")
    artifact_path_parser.add_argument(
        "--resolve-collision",
        action="store_true",
        help="Return first non-existing path if base exists.",
    )

    return parser


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _emit_json(data: dict, output: str | None) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def _cmd_extract_from_url(args: argparse.Namespace) -> int:
    try:
        local_path, repo_url = acquire_from_url(args.url)
        facts = extract_facts(local_path, repo_url=repo_url, source_type="github_url")
    except AcquireError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    _emit_json(facts.to_dict(), args.output)
    return 0


def _cmd_extract_from_path(args: argparse.Namespace) -> int:
    try:
        local_path = acquire_from_path(args.path)
        facts = extract_facts(
            local_path,
            repo_url=args.repo_url,
            source_type=args.source_type,
        )
    except AcquireError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    _emit_json(facts.to_dict(), args.output)
    return 0


def _cmd_unpack(args: argparse.Namespace) -> int:
    try:
        path = unpack_zip(args.zip, args.slug)
    except AcquireError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(str(path))
    return 0


def _cmd_compose_portfolio(args: argparse.Namespace) -> int:
    facts = ProjectFacts.from_dict(_load_json(args.facts))
    draft = compose_portfolio(facts)
    _emit_json(draft.to_dict(), args.output)
    return 0


def _cmd_write_artifact(args: argparse.Namespace) -> int:
    facts = ProjectFacts.from_dict(_load_json(args.facts))
    draft = PortfolioDraft.from_dict(_load_json(args.draft))
    approved = args.approved_by_user == "true"
    artifact = build_artifact(
        args.project_slug,
        facts,
        draft,
        approved_by_user=approved,
    )
    out_path = Path(args.output) if args.output else resolve_artifact_path(args.project_slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_portfolio_yaml(artifact), encoding="utf-8")
    print(str(out_path))
    return 0


def _cmd_artifact_path(args: argparse.Namespace) -> int:
    if args.resolve_collision:
        path = resolve_artifact_path(args.project_slug)
    else:
        path = artifact_path(args.project_slug)
    print(str(path))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    commands = {
        "extract-from-url": _cmd_extract_from_url,
        "extract-from-path": _cmd_extract_from_path,
        "unpack": _cmd_unpack,
        "compose-portfolio": _cmd_compose_portfolio,
        "write-artifact": _cmd_write_artifact,
        "artifact-path": _cmd_artifact_path,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())

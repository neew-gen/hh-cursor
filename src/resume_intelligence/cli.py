from __future__ import annotations

import argparse
import sys

from .runner import run_resume_intelligence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate resume intelligence artifact.")
    parser.add_argument(
        "--output",
        default="artifacts/resume-intelligence.md",
        help="Path to the generated Markdown artifact.",
    )
    parser.add_argument(
        "--max-sources",
        type=int,
        default=None,
        help="Limit how many configured sources are fetched.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Per-source fetch timeout in seconds.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_resume_intelligence(
        output_path=args.output,
        max_sources=args.max_sources,
        timeout=args.timeout,
    )
    print(
        f"Generated {result.artifact_path} "
        f"(sources ok: {result.successful_sources}/{result.requested_sources})"
    )
    return 0 if result.requested_sources and result.successful_sources >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

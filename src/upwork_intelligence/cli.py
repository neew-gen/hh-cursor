from __future__ import annotations

import argparse
import json
import sys

from .fetchers import DEFAULT_SOURCES_DIR, ingest_browser_text
from .registry import get_default_sources
from .runner import run_upwork_intelligence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Upwork intelligence artifact.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Fetch sources and write artifact (default).")
    run_parser.add_argument(
        "--output",
        default="artifacts/upwork-intelligence.md",
        help="Path to the generated Markdown artifact.",
    )
    run_parser.add_argument(
        "--max-sources",
        type=int,
        default=None,
        help="Limit how many configured sources are fetched.",
    )
    run_parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Per-source HTTP fetch timeout in seconds.",
    )
    run_parser.add_argument(
        "--sources-dir",
        default=DEFAULT_SOURCES_DIR,
        help="Directory with browser-cached source text files (<source-id>.txt).",
    )
    run_parser.add_argument(
        "--http-only",
        action="store_true",
        help="Skip browser cache and use HTTP fetch only.",
    )

    subparsers.add_parser("list-sources", help="List registry sources and cache file paths.")

    ingest_parser = subparsers.add_parser(
        "ingest-text",
        help="Normalize and store browser-extracted text for a source id.",
    )
    ingest_parser.add_argument("--source-id", required=True, help="Registry source id.")
    ingest_parser.add_argument("--input", required=True, help="Plain-text file from Browser Tab.")
    ingest_parser.add_argument(
        "--sources-dir",
        default=DEFAULT_SOURCES_DIR,
        help="Output directory for cached source text.",
    )

    parser.set_defaults(command="run")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    known_commands = {"run", "list-sources", "ingest-text"}
    if argv and argv[0] not in known_commands and argv[0] not in {"-h", "--help"}:
        argv = ["run", *argv]

    args = build_parser().parse_args(argv)

    if args.command == "list-sources":
        payload = [
            {
                "id": source.id,
                "title": source.title,
                "url": source.url,
                "cache_file": f"{DEFAULT_SOURCES_DIR}/{source.id}.txt",
            }
            for source in get_default_sources()
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "ingest-text":
        try:
            output = ingest_browser_text(
                source_id=args.source_id,
                input_path=args.input,
                sources_dir=args.sources_dir,
            )
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        print(f"Ingested {args.source_id} -> {output}")
        return 0

    result = run_upwork_intelligence(
        output_path=args.output,
        max_sources=args.max_sources,
        timeout=args.timeout,
        sources_dir=None if args.http_only else args.sources_dir,
        prefer_cache=not args.http_only,
    )
    print(
        f"Generated {result.artifact_path} "
        f"(sources ok: {result.successful_sources}/{result.requested_sources})"
    )
    return 0 if result.requested_sources and result.successful_sources >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

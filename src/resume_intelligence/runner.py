from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .fetchers import fetch_source
from .models import PipelineRun
from .registry import get_default_sources
from .report import render_markdown
from .synthesis import build_report


def run_resume_intelligence(
    output_path: str = "artifacts/resume-intelligence.md",
    max_sources: int | None = None,
    timeout: int = 15,
) -> PipelineRun:
    started_at = datetime.now(timezone.utc)
    sources = get_default_sources()
    if max_sources is not None:
        sources = sources[:max_sources]

    results = [fetch_source(source, timeout=timeout) for source in sources]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    report = build_report(results=results, artifact_path=str(output), generated_at=started_at)
    output.write_text(render_markdown(report), encoding="utf-8")

    finished_at = datetime.now(timezone.utc)
    successful = sum(1 for result in results if result.status == "ok")
    failed = len(results) - successful
    return PipelineRun(
        started_at=started_at,
        finished_at=finished_at,
        requested_sources=len(results),
        successful_sources=successful,
        failed_sources=failed,
        artifact_path=str(output),
    )

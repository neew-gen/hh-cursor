from datetime import datetime, timezone
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from upwork_intelligence.fetchers import ingest_browser_text, fetch_source
from upwork_intelligence.models import SourceDescriptor, SourceFetchResult
from upwork_intelligence.runner import run_upwork_intelligence


class UpworkRunnerTests(unittest.TestCase):
    def test_run_upwork_intelligence_writes_artifact(self) -> None:
        source = SourceDescriptor(
            id="upwork-help-proposals",
            title="How to submit a proposal on Upwork",
            url="https://support.upwork.com/hc/en-us/articles/example",
            source_class="upwork_help",
            trust_tier="primary",
            topics=["proposals"],
        )
        fetch_result = SourceFetchResult(
            descriptor=source,
            status="ok",
            fetched_at=datetime.now(timezone.utc),
            text="Clients skim proposals and expect a personalized cover letter with Uma draft tips.",
            fetch_channel="browser_cache",
        )

        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "upwork-intelligence.md"
            with patch("upwork_intelligence.runner.fetch_source", return_value=fetch_result):
                with patch("upwork_intelligence.runner.get_default_sources", return_value=[source]):
                    result = run_upwork_intelligence(
                        output_path=str(output_path),
                        max_sources=1,
                        timeout=1,
                        sources_dir=Path(tmp) / "cache",
                    )

            content = output_path.read_text(encoding="utf-8")
            self.assertTrue(output_path.is_file())
            self.assertEqual(result.artifact_path, str(output_path))
            self.assertEqual(result.successful_sources, 1)
            self.assertIn("# Upwork Intelligence", content)
            self.assertIn("## WhatToWriteInProposals", content)

    def test_fetch_source_prefers_browser_cache(self) -> None:
        source = SourceDescriptor(
            id="upwork-help-proposals",
            title="How to submit a proposal on Upwork",
            url="https://support.upwork.com/hc/en-us/articles/example",
            source_class="upwork_help",
            trust_tier="primary",
            topics=["proposals"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.txt"
            raw.write_text(
                "Write your cover letter. Describe what you can do for the client. "
                "Answer screening questions. Use Uma to improve your proposal draft.",
                encoding="utf-8",
            )
            ingest_browser_text(
                source_id="upwork-help-proposals",
                input_path=raw,
                sources_dir=tmp,
            )

            result = fetch_source(source, timeout=1, sources_dir=tmp, prefer_cache=True)
            self.assertEqual(result.status, "ok")
            self.assertEqual(result.fetch_channel, "browser_cache")
            self.assertIn("cover letter", result.text.lower())


if __name__ == "__main__":
    unittest.main()

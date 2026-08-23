from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from upwork_intelligence.models import RecommendationItem, UpworkIntelligenceReport
from upwork_intelligence.report import render_markdown
from upwork_profile_create.cli import build_parser
from upwork_profile_create.loader import load_inputs, load_intelligence


class UpworkProfileCreateLoaderTests(unittest.TestCase):
    def test_load_intelligence_reads_what_to_write_in_proposals(self) -> None:
        report = UpworkIntelligenceReport(
            summary_points=["Summary point"],
            proposal_review_findings=[],
            proposal_recommendations=[
                RecommendationItem(
                    recommendation_text="Personalize the cover letter to the job post.",
                    target="proposal_content",
                    rationale="Derived from primary evidence",
                    confidence="high",
                    supporting_sources=["upwork-help-proposals"],
                )
            ],
            profile_recommendations=[
                RecommendationItem(
                    recommendation_text="Keep title, overview, and portfolio aligned.",
                    target="profile",
                    rationale="Derived from primary evidence",
                    confidence="medium",
                    supporting_sources=["upwork-profile-tips"],
                )
            ],
            conflicts=[],
            source_notes=[
                "`upwork-help-proposals` | primary | upwork_help | https://example.com"
            ],
            limitations=["Recommendations reflect the run timestamp."],
            generated_at=None,
            artifact_path="artifacts/upwork-intelligence.md",
        )

        with tempfile.TemporaryDirectory() as tmp:
            intel_path = Path(tmp) / "upwork-intelligence.md"
            intel_path.write_text(render_markdown(report), encoding="utf-8")

            brief = load_intelligence(intel_path)

            self.assertEqual(len(brief.what_to_write), 1)
            self.assertIn("Personalize the cover letter", brief.what_to_write[0])
            self.assertEqual(len(brief.how_to_build_profile), 1)
            self.assertIn("Keep title, overview", brief.how_to_build_profile[0])

    def test_load_inputs_exposes_proposal_guidance(self) -> None:
        profile_path = Path("tests/fixtures/upwork-profile-sample.yaml")
        report = UpworkIntelligenceReport(
            summary_points=["Summary point"],
            proposal_review_findings=[],
            proposal_recommendations=[
                RecommendationItem(
                    recommendation_text="Lead with relevant client outcomes.",
                    target="proposal_content",
                    rationale="Derived from primary evidence",
                    confidence="high",
                    supporting_sources=["upwork-help-proposals"],
                )
            ],
            profile_recommendations=[],
            conflicts=[],
            source_notes=[
                "`upwork-help-proposals` | primary | upwork_help | https://example.com"
            ],
            limitations=[],
            generated_at=None,
            artifact_path="artifacts/upwork-intelligence.md",
        )

        with tempfile.TemporaryDirectory() as tmp:
            intel_path = Path(tmp) / "upwork-intelligence.md"
            intel_path.write_text(render_markdown(report), encoding="utf-8")

            result = load_inputs(profile_path, intel_path)

            self.assertTrue(result["intelligence_available"])
            self.assertEqual(len(result["what_to_write"]), 1)
            self.assertIn("client outcomes", result["what_to_write"][0])

    def test_compose_cli_accepts_skill_fill_modes(self) -> None:
        parser = build_parser()
        for fill_mode in ("create_new", "edit_existing"):
            with self.subTest(fill_mode=fill_mode):
                args = parser.parse_args(
                    [
                        "compose",
                        "--profile",
                        "tests/fixtures/upwork-profile-sample.yaml",
                        "--draft",
                        "tmp/draft.json",
                        "--fill-mode",
                        fill_mode,
                    ]
                )
                self.assertEqual(args.fill_mode, fill_mode)


if __name__ == "__main__":
    unittest.main()

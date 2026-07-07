from datetime import datetime, timezone
import unittest

from resume_intelligence.models import RecommendationItem, ResumeIntelligenceReport
from resume_intelligence.report import render_markdown


class ReportRenderingTests(unittest.TestCase):
    def test_render_markdown_includes_required_sections(self) -> None:
        report = ResumeIntelligenceReport(
            summary_points=["Summary point"],
            screening_findings=[
                RecommendationItem(
                    recommendation_text="Recruiters scan preview fields first.",
                    target="screening",
                    rationale="Derived from primary evidence",
                    confidence="high",
                    supporting_sources=["hh-source"],
                )
            ],
            content_recommendations=[
                RecommendationItem(
                    recommendation_text="Use achievements and vacancy keywords.",
                    target="content",
                    rationale="Derived from primary evidence",
                    confidence="high",
                    supporting_sources=["hh-source"],
                )
            ],
            format_recommendations=[
                RecommendationItem(
                    recommendation_text="Keep the structure simple and parseable.",
                    target="format",
                    rationale="Derived from primary evidence",
                    confidence="medium",
                    supporting_sources=["vendor-source"],
                )
            ],
            conflicts=["Secondary sources disagree on document format preferences."],
            source_notes=["`hh-source` | primary | hh_help | https://example.com"],
            limitations=["One source was unavailable."],
            generated_at=datetime.now(timezone.utc),
            artifact_path="artifacts/resume-intelligence.md",
        )

        markdown = render_markdown(report)

        self.assertIn("# Resume Intelligence", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("## HowHRAndATSProcessResumesNow", markdown)
        self.assertIn("## WhatToWrite", markdown)
        self.assertIn("## HowToBuildResume", markdown)
        self.assertIn("## SourceQualityAndConflicts", markdown)
        self.assertIn("## Sources", markdown)
        self.assertIn("## FreshnessAndLimitations", markdown)


if __name__ == "__main__":
    unittest.main()

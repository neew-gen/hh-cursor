from datetime import datetime, timezone
import unittest

from upwork_intelligence.models import RecommendationItem, UpworkIntelligenceReport
from upwork_intelligence.report import render_markdown


class UpworkReportRenderingTests(unittest.TestCase):
    def test_render_markdown_includes_required_sections(self) -> None:
        report = UpworkIntelligenceReport(
            summary_points=["Summary point"],
            proposal_review_findings=[
                RecommendationItem(
                    recommendation_text="Clients skim proposals against profile signals.",
                    target="proposal_review",
                    rationale="Derived from primary evidence",
                    confidence="high",
                    supporting_sources=["upwork-help-proposals"],
                )
            ],
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
            conflicts=["Uma guidance appears in only part of the source set."],
            source_notes=[
                "`upwork-help-proposals` | primary | upwork_help | https://support.upwork.com/example"
            ],
            limitations=["One source was unavailable."],
            generated_at=datetime.now(timezone.utc),
            artifact_path="artifacts/upwork-intelligence.md",
        )

        markdown = render_markdown(report)

        self.assertIn("# Upwork Intelligence", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("## HowClientsReviewProposalsNow", markdown)
        self.assertIn("## WhatToWriteInProposals", markdown)
        self.assertIn("## HowToBuildProfile", markdown)
        self.assertIn("## SourceQualityAndConflicts", markdown)
        self.assertIn("## Sources", markdown)
        self.assertIn("## FreshnessAndLimitations", markdown)


if __name__ == "__main__":
    unittest.main()

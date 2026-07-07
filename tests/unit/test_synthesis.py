from datetime import datetime, timezone
import unittest

from resume_intelligence.models import SourceDescriptor, SourceFetchResult
from resume_intelligence.synthesis import build_report


class SynthesisTests(unittest.TestCase):
    def test_build_report_populates_sections(self) -> None:
        source = SourceDescriptor(
            id="hh-source",
            title="HH",
            url="https://example.com",
            source_class="hh_help",
            trust_tier="primary",
            topics=["screening", "keywords", "formatting"],
        )
        result = SourceFetchResult(
            descriptor=source,
            status="ok",
            fetched_at=datetime.now(timezone.utc),
            text=(
                "Рекрутер смотрит превью резюме и обращает внимание на опыт и навыки. "
                "Адаптируйте резюме под вакансию и добавляйте ключевые навыки. "
                "Используйте понятные разделы и простой формат документа."
            ),
        )

        report = build_report(
            results=[result],
            artifact_path="artifacts/resume-intelligence.md",
            generated_at=datetime.now(timezone.utc),
        )

        self.assertTrue(report.screening_findings)
        self.assertTrue(report.content_recommendations)
        self.assertTrue(report.format_recommendations)
        self.assertTrue(report.source_notes)


if __name__ == "__main__":
    unittest.main()

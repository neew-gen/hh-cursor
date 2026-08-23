from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from upwork_proposal.composer import compose_proposal_plan
from upwork_proposal.slug import job_slug_from_snapshot, job_slug_from_url
from upwork_proposal.validator import validate_proposal_plan


class UpworkProposalSlugTests(unittest.TestCase):
    def test_slug_from_url_with_id(self) -> None:
        self.assertEqual(
            job_slug_from_url("https://www.upwork.com/jobs/~0123456789abcdef"),
            "job-0123456789abcdef",
        )

    def test_slug_from_snapshot_fallback(self) -> None:
        slug = job_slug_from_snapshot("", "TechStartup Inc", "Senior Frontend Developer")
        self.assertTrue(slug.startswith("job-"))


class UpworkProposalComposerTests(unittest.TestCase):
    def _profile_path(self) -> Path:
        return Path("tests/fixtures/upwork-profile-sample.yaml")

    def _cover_letter_text(self) -> str:
        return (
            "Hi there — I was drawn to your dashboard project because it aligns with my "
            "experience building TypeScript frontends and REST integrations. "
            "At Acme Corp I developed product interfaces on Vue and integrated REST APIs, "
            "improving page performance and maintaining a shared UI Kit. "
            "In my current role at Beta LLC I lead code reviews, ship internal services, "
            "and work daily with TypeScript, Vue.js, and Docker. "
            "Your stack mentions React and TypeScript — my JavaScript and TypeScript "
            "background maps well to React dashboards and API-heavy products. "
            "I would welcome a short call to discuss milestones and timeline. "
            "Happy to share relevant portfolio samples if helpful."
        )

    def test_compose_creates_proposal_plan(self) -> None:
        profile_path = self._profile_path()
        job_path = Path("tests/fixtures/upwork-job-extract.json")

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps(
                    {
                        "cover_letter_text": self._cover_letter_text(),
                        "language": "en",
                        "rewrite_applied": True,
                        "screening_answers": [
                            {
                                "question": "Describe your experience with React dashboards.",
                                "answer": "Built multiple dashboards with Vue and TypeScript; React is adjacent.",
                            },
                            {
                                "question": "What is your hourly rate?",
                                "answer": "$60/hour",
                            },
                        ],
                        "contract_terms": {
                            "bid_type": "hourly",
                            "hourly_rate": "$60",
                            "duration": "1 to 3 months",
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            plan = compose_proposal_plan(
                profile_path=profile_path,
                job_path=job_path,
                draft_path=draft_path,
            )
            self.assertEqual(plan.job.title, "Senior Frontend Developer")
            self.assertEqual(plan.target_role, "Frontend Developer")
            self.assertGreaterEqual(plan.cover_letter.char_count, 300)
            errors = validate_proposal_plan(plan, profile_path)
            self.assertEqual(errors, [])

    def test_compose_rejects_empty_cover_letter(self) -> None:
        profile_path = self._profile_path()
        job_path = Path("tests/fixtures/upwork-job-extract.json")

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(json.dumps({"cover_letter_text": ""}), encoding="utf-8")
            with self.assertRaises(ValueError):
                compose_proposal_plan(
                    profile_path=profile_path,
                    job_path=job_path,
                    draft_path=draft_path,
                )


if __name__ == "__main__":
    unittest.main()

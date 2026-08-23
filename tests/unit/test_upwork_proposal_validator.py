from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from upwork_proposal.composer import compose_proposal_plan
from upwork_proposal.validator import (
    MIN_COVER_LETTER_LENGTH,
    MAX_COVER_LETTER_LENGTH,
    validate_proposal_plan,
)


class UpworkProposalValidatorTests(unittest.TestCase):
    def _profile_path(self) -> Path:
        return Path("tests/fixtures/upwork-profile-sample.yaml")

    def _compose_plan(self, cover_letter_text: str, screening_answers: list | None = None) -> object:
        profile_path = self._profile_path()
        job_path = Path("tests/fixtures/upwork-job-extract.json")

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_data = {
                "cover_letter_text": cover_letter_text,
                "language": "en",
            }
            if screening_answers is not None:
                draft_data["screening_answers"] = screening_answers

            draft_path.write_text(json.dumps(draft_data, ensure_ascii=False), encoding="utf-8")
            return compose_proposal_plan(
                profile_path=profile_path,
                job_path=job_path,
                draft_path=draft_path,
            )

    def test_validator_rejects_unknown_employer(self) -> None:
        profile_path = self._profile_path()
        bad_letter = (
            "Hello — I worked at FakeCorp building Vue dashboards with TypeScript. "
            "I have strong JavaScript skills and REST API experience. "
            "Ready to discuss your project timeline and deliverables. "
        ) * 4

        plan = self._compose_plan(bad_letter)
        errors = validate_proposal_plan(plan, profile_path)
        self.assertTrue(any("employers not in profile" in e for e in errors))

    def test_validator_rejects_short_cover_letter(self) -> None:
        profile_path = self._profile_path()
        short_letter = "Too short proposal text."

        plan = self._compose_plan(short_letter)
        errors = validate_proposal_plan(plan, profile_path)
        self.assertTrue(
            any(str(MIN_COVER_LETTER_LENGTH) in e for e in errors)
        )

    def test_validator_rejects_long_cover_letter(self) -> None:
        profile_path = self._profile_path()
        long_letter = "A" * (MAX_COVER_LETTER_LENGTH + 1)

        plan = self._compose_plan(long_letter)
        errors = validate_proposal_plan(plan, profile_path)
        self.assertTrue(
            any(str(MAX_COVER_LETTER_LENGTH) in e for e in errors)
        )

    def test_validator_requires_screening_answers(self) -> None:
        profile_path = self._profile_path()
        letter = (
            "Hello — your dashboard role matches my TypeScript and JavaScript background. "
            "At Acme Corp I built interfaces and integrated REST APIs with Vue. "
            "At Beta LLC I ship internal services and conduct code reviews daily. "
            "I can align on milestones and communicate progress clearly. "
            "Happy to start with a short discovery call this week."
        ) * 2

        plan = self._compose_plan(letter, screening_answers=[])
        errors = validate_proposal_plan(plan, profile_path)
        self.assertTrue(any("screening question unanswered" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

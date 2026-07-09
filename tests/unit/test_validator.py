from __future__ import annotations

import unittest
from unittest.mock import patch

from resume_create.models import FillPlan, FillPlanMeta
from resume_create.validator import normalize_date, validate_fill_plan
from resume_profile.models import ResumeProfile, SkillEntry, WorkExperienceEntry


class ValidatorTests(unittest.TestCase):
    def test_normalize_russian_month_date(self) -> None:
        self.assertEqual(normalize_date("Июнь 2025"), "06.2025")
        self.assertEqual(normalize_date("2025-06"), "06.2025")

    def test_validate_rejects_extra_company(self) -> None:
        source = ResumeProfile(
            target_role="Developer",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(company="Acme", position="Dev", start_date="2020-01")
            ],
            skills_hard=[SkillEntry(name="Python")],
        )
        candidate = ResumeProfile(
            target_role="Developer",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(
                    company="Other Co",
                    position="Dev",
                    start_date="2020-01",
                )
            ],
            skills_hard=[SkillEntry(name="Python")],
        )
        fill_plan = FillPlan(profile=candidate, meta=FillPlanMeta())
        with patch(
            "resume_create.validator.load_profile",
            return_value=source,
        ):
            errors = validate_fill_plan(fill_plan, "ignored")
        self.assertTrue(any("companies differ" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

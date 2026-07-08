import unittest

from resume_profile.gaps import compute_gaps, is_complete
from resume_profile.models import (
    EducationEntry,
    ResumeProfile,
    SkillEntry,
    WorkExperienceEntry,
)


class GapDetectionTests(unittest.TestCase):
    def test_empty_profile_has_mvp_gaps(self):
        profile = ResumeProfile()
        gaps = compute_gaps(profile)
        field_ids = {gap.field_id for gap in gaps}
        self.assertIn("target_role", field_ids)
        self.assertIn("work_experience_status", field_ids)
        self.assertIn("skills.hard", field_ids)

    def test_skip_q1_questionnaire_only_complete(self):
        profile = ResumeProfile(
            input_mode="questionnaire_only",
            target_role="Backend Developer",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(
                    company="Acme",
                    position="Developer",
                    start_date="2021-01",
                    end_date=None,
                    is_current=True,
                    description="Built APIs",
                    provenance="from_user_answer",
                )
            ],
            skills_hard=[
                SkillEntry(
                    name="Python",
                    level="advanced",
                    provenance="from_user_answer",
                )
            ],
            education=[
                EducationEntry(
                    institution="MSU",
                    degree="Bachelor",
                    specialty="CS",
                    graduation_year=2020,
                    provenance="from_user_answer",
                )
            ],
            about_me="Backend developer with API experience.",
        )
        self.assertTrue(is_complete(profile))
        self.assertNotIn("about_me", {g.field_id for g in compute_gaps(profile)})

    def test_no_experience_status_is_complete(self):
        profile = ResumeProfile(
            target_role="Junior QA",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="Testing", level="medium")],
            no_formal_education=True,
        )
        self.assertTrue(is_complete(profile))


    def test_about_me_gap_when_empty(self):
        profile = ResumeProfile(
            target_role="Developer",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="Python", level="medium")],
            no_formal_education=True,
        )
        gaps = compute_gaps(profile)
        field_ids = {gap.field_id for gap in gaps}
        self.assertIn("about_me", field_ids)
        self.assertTrue(is_complete(profile))

    def test_no_about_me_gap_when_filled(self):
        profile = ResumeProfile(
            target_role="Developer",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="Python", level="medium")],
            no_formal_education=True,
            about_me="Опытный разработчик.",
        )
        field_ids = {gap.field_id for gap in compute_gaps(profile)}
        self.assertNotIn("about_me", field_ids)

    def test_append_mode_adds_skills_gap_when_empty(self):
        profile = ResumeProfile(
            target_role="Developer",
            work_experience_status="none",
            skills_hard=[],
            no_formal_education=True,
        )
        meta = {"skills_mode": "append", "collect_skills": True}
        gaps = compute_gaps(profile, meta=meta)
        self.assertIn("skills.hard", {gap.field_id for gap in gaps})

    def test_append_mode_skips_skills_gap_when_new_skills_present(self):
        profile = ResumeProfile(
            target_role="Developer",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="React", level="medium")],
            no_formal_education=True,
        )
        meta = {"skills_mode": "append", "collect_skills": True}
        field_ids = {gap.field_id for gap in compute_gaps(profile, meta=meta)}
        self.assertNotIn("skills.hard", field_ids)


if __name__ == "__main__":
    unittest.main()

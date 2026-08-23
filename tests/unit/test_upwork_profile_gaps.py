import unittest

from freelancer_core.models import EducationEntry, WorkExperienceEntry
from upwork_profile.gaps import compute_gaps, is_complete
from upwork_profile.models import UpworkProfile


class UpworkGapDetectionTests(unittest.TestCase):
    def test_empty_profile_has_mvp_gaps(self):
        profile = UpworkProfile()
        gaps = compute_gaps(profile)
        field_ids = {gap.field_id for gap in gaps}
        self.assertIn("profile_title", field_ids)
        self.assertIn("overview", field_ids)
        self.assertIn("hourly_rate", field_ids)
        self.assertIn("skills", field_ids)
        self.assertIn("work_experience_status", field_ids)

    def test_complete_profile(self):
        profile = UpworkProfile(
            input_mode="questionnaire_only",
            profile_title="Full Stack Developer",
            overview="Experienced developer building web applications.",
            hourly_rate="75",
            skills=["Python", "React"],
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
            education=[
                EducationEntry(
                    institution="MIT",
                    degree="Bachelor",
                    specialty="CS",
                    graduation_year=2020,
                    provenance="from_user_answer",
                )
            ],
        )
        self.assertTrue(is_complete(profile))
        self.assertNotIn("portfolio_links", {g.field_id for g in compute_gaps(profile)})

    def test_no_experience_status_is_complete(self):
        profile = UpworkProfile(
            profile_title="Junior QA",
            overview="QA specialist with manual testing experience.",
            hourly_rate="30",
            skills=["Testing"],
            work_experience_status="none",
        )
        self.assertTrue(is_complete(profile))

    def test_education_gap_when_empty(self):
        profile = UpworkProfile(
            profile_title="Developer",
            overview="Backend developer.",
            hourly_rate="50",
            skills=["Python"],
            work_experience_status="none",
        )
        gaps = compute_gaps(profile)
        field_ids = {gap.field_id for gap in gaps}
        self.assertIn("education", field_ids)
        self.assertTrue(is_complete(profile))

    def test_education_gap_absent_when_filled(self):
        profile = UpworkProfile(
            profile_title="Developer",
            overview="Backend developer.",
            hourly_rate="50",
            skills=["Python"],
            work_experience_status="none",
            education=[
                EducationEntry(
                    institution="MSU",
                    degree="Bachelor",
                    specialty="CS",
                    graduation_year=2019,
                )
            ],
        )
        field_ids = {gap.field_id for gap in compute_gaps(profile)}
        self.assertNotIn("education", field_ids)


if __name__ == "__main__":
    unittest.main()

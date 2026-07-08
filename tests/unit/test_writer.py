import unittest

from resume_profile.models import (
    EducationEntry,
    ResumeProfile,
    SkillEntry,
    WorkExperienceEntry,
)
from resume_profile.writer import (
    finalize_profile,
    profile_from_dict,
    profile_to_dict,
    render_yaml,
)
from resume_profile.yaml_io import parse_artifact_yaml


class WriterTests(unittest.TestCase):
    def test_render_yaml_contains_required_sections(self):
        profile = ResumeProfile(
            collected_at="2026-07-08T00:00:00+00:00",
            input_mode="questionnaire_only",
            target_role="Backend Developer",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="Python", level="advanced")],
            no_formal_education=True,
            limitations=["Resume link skipped"],
        )
        yaml_text = render_yaml(finalize_profile(profile))
        self.assertIn("target_role:", yaml_text)
        self.assertIn("work_experience:", yaml_text)
        self.assertIn("skills:", yaml_text)
        self.assertIn("education:", yaml_text)
        self.assertNotIn("key_phrases:", yaml_text)

    def test_yaml_roundtrip(self):
        original = ResumeProfile(
            target_role="Analyst",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(
                    company="Bank",
                    position="Analyst",
                    start_date="2020-06",
                    description="Reports",
                )
            ],
            skills_hard=[SkillEntry(name="Excel", level="medium")],
            education=[
                EducationEntry(
                    institution="HSE",
                    degree="Master",
                    specialty="Economics",
                    graduation_year=2019,
                )
            ],
        )
        yaml_text = render_yaml(finalize_profile(original))
        restored = profile_from_dict(parse_artifact_yaml(yaml_text))
        self.assertEqual(restored.target_role, "Analyst")
        self.assertEqual(len(restored.work_experience), 1)
        self.assertEqual(restored.skills_hard[0].name, "Excel")


if __name__ == "__main__":
    unittest.main()

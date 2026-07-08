import unittest

from resume_profile.models import ResumeProfile
from resume_profile.questionnaire import (
    DEFER_OPTION_ID,
    DEFER_OPTION_LABEL,
    build_ask_options,
    gap_question,
)


class QuestionnaireTests(unittest.TestCase):
    def test_target_role_question_without_link(self):
        profile = ResumeProfile(input_mode="questionnaire_only")
        self.assertEqual(gap_question("target_role", profile), "Какая ваша желаемая должность?")

    def test_target_role_question_with_link(self):
        profile = ResumeProfile(
            input_mode="questionnaire_with_link",
            resume_link="https://hh.ru/resume/abc",
        )
        self.assertEqual(
            gap_question("target_role", profile),
            "Какая желаемая должность указана в резюме?",
        )

    def test_defer_option_is_always_last_for_open_field(self):
        profile = ResumeProfile()
        options = build_ask_options("target_role", profile)
        self.assertEqual(len(options), 1)
        self.assertEqual(options[-1]["id"], DEFER_OPTION_ID)
        self.assertEqual(options[-1]["label"], DEFER_OPTION_LABEL)

    def test_defer_option_is_last_when_draft_has_suggestion(self):
        profile = ResumeProfile(target_role="Backend Developer")
        options = build_ask_options("target_role", profile)
        self.assertEqual(options[0]["label"], "Backend Developer")
        self.assertEqual(options[-1]["id"], DEFER_OPTION_ID)

    def test_fixed_field_has_no_defer_option(self):
        profile = ResumeProfile()
        options = build_ask_options("work_experience_status", profile)
        labels = [option["label"] for option in options]
        self.assertNotIn(DEFER_OPTION_LABEL, labels)
        self.assertEqual(len(options), 2)


if __name__ == "__main__":
    unittest.main()

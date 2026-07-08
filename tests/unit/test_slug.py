import unittest

from resume_profile.draft import SKILLS_MODE_APPEND, merge_skill_entries
from resume_profile.models import SkillEntry
from resume_profile.slug import slugify_target_role


class SlugTests(unittest.TestCase):
    def test_latin_role(self):
        self.assertEqual(
            slugify_target_role("Frontend Developer (Vue)"),
            "frontend-developer-vue",
        )

    def test_cyrillic_role(self):
        self.assertEqual(
            slugify_target_role("Старший Frontend-разработчик"),
            "starshiy-frontend-razrabotchik",
        )


class MergeSkillsTests(unittest.TestCase):
    def test_append_deduplicates_by_name(self):
        existing = [SkillEntry(name="Vue.js", level="medium")]
        incoming = [
            SkillEntry(name="vue.js", level="advanced"),
            SkillEntry(name="React", level="medium"),
        ]
        merged = merge_skill_entries(existing, incoming, mode=SKILLS_MODE_APPEND)
        names = [skill.name for skill in merged]
        self.assertEqual(names, ["Vue.js", "React"])


if __name__ == "__main__":
    unittest.main()

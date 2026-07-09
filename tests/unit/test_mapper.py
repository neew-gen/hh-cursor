from __future__ import annotations

import unittest

from resume_create.mapper import format_date_for_form, list_form_mappings, skill_level_label


class MapperTests(unittest.TestCase):
    def test_skill_level_labels(self) -> None:
        self.assertEqual(skill_level_label("basic"), "Базовый")
        self.assertEqual(skill_level_label("advanced"), "Продвинутый")

    def test_form_mappings_include_required_blocks(self) -> None:
        field_ids = {item["field_id"] for item in list_form_mappings()}
        self.assertIn("target_role", field_ids)
        self.assertIn("skills.hard", field_ids)
        self.assertIn("about_me", field_ids)

    def test_format_date_for_form(self) -> None:
        self.assertEqual(format_date_for_form("Сентябрь 2023"), "09.2023")


if __name__ == "__main__":
    unittest.main()

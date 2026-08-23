from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from upwork_profile_create.composer import compose_fill_plan
from upwork_profile_create.loader import load_profile
from upwork_profile_create.validator import validate_fill_plan


class UpworkProfileCreateComposerTests(unittest.TestCase):
    def _sample_profile_path(self) -> Path:
        return Path("tests/fixtures/upwork-profile-sample.yaml")

    def test_compose_merges_rewritten_overview(self) -> None:
        profile_path = self._sample_profile_path()
        source = load_profile(profile_path)

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps(
                    {
                        "overview": "Rewritten overview for Upwork profile.",
                        "profile_title": source.profile_title,
                        "skills": list(source.skills),
                        "work_experience": [
                            {"description": entry.description}
                            for entry in source.work_experience
                        ],
                        "rewrite_applied": {
                            "overview": True,
                            "profile_title": False,
                            "work_experience_descriptions": True,
                            "skills_tags": False,
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            fill_plan = compose_fill_plan(
                profile_path=profile_path,
                draft_path=draft_path,
                fill_mode="edit_existing",
            )
            self.assertEqual(fill_plan.profile.overview, "Rewritten overview for Upwork profile.")
            self.assertTrue(fill_plan.meta.rewrite_applied.overview)
            errors = validate_fill_plan(fill_plan, profile_path)
            self.assertEqual(errors, [])

    def test_compose_rejects_mismatched_experience_count(self) -> None:
        profile_path = self._sample_profile_path()

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps({"work_experience": [{"description": "only one"}]}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                compose_fill_plan(
                    profile_path=profile_path,
                    draft_path=draft_path,
                    fill_mode="create_new",
                )


if __name__ == "__main__":
    unittest.main()

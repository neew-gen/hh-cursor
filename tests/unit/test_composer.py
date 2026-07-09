from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from resume_create.composer import compose_fill_plan
from resume_create.validator import validate_fill_plan
from resume_profile.artifacts import load_artifact


class ComposerTests(unittest.TestCase):
    def _sample_profile_path(self) -> Path:
        path = Path("artifacts/resume-profile/frontend-developer-vue.yaml")
        if not path.is_file():
            self.skipTest("sample profile artifact not available")
        return path

    def test_compose_merges_rewritten_about_me(self) -> None:
        profile_path = self._sample_profile_path()
        source = load_artifact(profile_path)

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps(
                    {
                        "about_me": "Переписанный блок обо мне.",
                        "work_experience": [
                            {"description": entry.description}
                            for entry in source.work_experience
                        ],
                        "rewrite_applied": {
                            "about_me": True,
                            "work_experience_descriptions": True,
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            fill_plan = compose_fill_plan(
                profile_path=profile_path,
                draft_path=draft_path,
                fill_mode="create_new",
            )
            self.assertEqual(fill_plan.profile.about_me, "Переписанный блок обо мне.")
            self.assertTrue(fill_plan.meta.rewrite_applied.about_me)
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

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resume_create.loader import load_intelligence, load_inputs


class LoaderTests(unittest.TestCase):
    def test_load_intelligence_extracts_high_confidence_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            intel_path = Path(tmp) / "intel.md"
            intel_path.write_text(
                """# Resume Intelligence

_Generated at: 2026-07-07T08:45:01+00:00_

## WhatToWrite
- [high] Опыт лучше описывать через конкретные результаты.
- [low] Игнорировать низкую уверенность.

## HowToBuildResume
- [high] Используйте простую структуру.

## Sources
- `hh-knowledge-create-resume` | primary | hh_help | https://example.com

## FreshnessAndLimitations
- Рекомендации актуальны на момент запуска.
""",
                encoding="utf-8",
            )
            brief = load_intelligence(intel_path)
            self.assertEqual(brief.generated_at, "2026-07-07T08:45:01+00:00")
            self.assertEqual(len(brief.what_to_write), 1)
            self.assertIn("конкретные результаты", brief.what_to_write[0])
            self.assertEqual(brief.source_ids, ["hh-knowledge-create-resume"])

    def test_load_inputs_uses_profile_path(self) -> None:
        profile_path = Path("artifacts/resume-profile/frontend-developer-vue.yaml")
        if not profile_path.is_file():
            self.skipTest("sample profile artifact not available")
        result = load_inputs(profile_path)
        self.assertEqual(result["profile_path"], str(profile_path))
        self.assertTrue(result["target_role"])


if __name__ == "__main__":
    unittest.main()

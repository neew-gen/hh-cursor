from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from job_apply.composer import compose_application_plan
from job_apply.slug import vacancy_slug_from_snapshot, vacancy_slug_from_url
from job_apply.validator import validate_application_plan
from resume_profile.artifacts import load_artifact


class JobApplySlugTests(unittest.TestCase):
    def test_slug_from_url_with_id(self) -> None:
        self.assertEqual(
            vacancy_slug_from_url("https://hh.ru/vacancy/12345678"),
            "vacancy-12345678",
        )

    def test_slug_from_snapshot_fallback(self) -> None:
        slug = vacancy_slug_from_snapshot("", "Acme Corp", "Frontend Dev")
        self.assertTrue(slug.startswith("vacancy-"))


class JobApplyComposerTests(unittest.TestCase):
    def _profile_path(self) -> Path:
        path = Path("artifacts/resume-profile/frontend-developer.yaml")
        if not path.is_file():
            self.skipTest("sample profile artifact not available")
        return path

    def _cover_letter_text(self) -> str:
        return (
            "Меня заинтересовала вакансия Frontend-разработчика в ТехКомпании — "
            "хочу применить опыт с Vue и TypeScript в вашем продукте. "
            "В Acme Corp разрабатывал систему учёта на Vue и Nuxt, "
            "интегрировал API и оптимизировал скорость страниц. "
            "В текущей роли внедрил FSD и UI Kit, проводил код-ревью и онбординг. "
            "Мой стек включает JavaScript, TypeScript, Vue и REST — это совпадает с вашими "
            "требованиями к коммерческой разработке и работе с API. "
            "Буду рад обсудить, как мой опыт поможет команде. "
            "Готов созвониться в удобное время."
        )

    def test_compose_creates_application_plan(self) -> None:
        profile_path = self._profile_path()
        vacancy_path = Path("tests/fixtures/vacancy-extract.json")

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps(
                    {
                        "cover_letter_text": self._cover_letter_text(),
                        "language": "ru",
                        "rewrite_applied": True,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            plan = compose_application_plan(
                profile_path=profile_path,
                vacancy_path=vacancy_path,
                draft_path=draft_path,
            )
            self.assertEqual(plan.vacancy.title, "Frontend-разработчик")
            self.assertEqual(plan.target_role, "Frontend Developer")
            self.assertGreaterEqual(plan.cover_letter.char_count, 400)
            errors = validate_application_plan(plan, profile_path)
            self.assertEqual(errors, [])

    def test_compose_rejects_empty_cover_letter(self) -> None:
        profile_path = self._profile_path()
        vacancy_path = Path("tests/fixtures/vacancy-extract.json")

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(json.dumps({"cover_letter_text": ""}), encoding="utf-8")
            with self.assertRaises(ValueError):
                compose_application_plan(
                    profile_path=profile_path,
                    vacancy_path=vacancy_path,
                    draft_path=draft_path,
                )


class JobApplyValidatorTests(unittest.TestCase):
    def _profile_path(self) -> Path:
        path = Path("artifacts/resume-profile/frontend-developer.yaml")
        if not path.is_file():
            self.skipTest("sample profile artifact not available")
        return path

    def test_validator_rejects_unknown_employer(self) -> None:
        profile_path = self._profile_path()
        vacancy_path = Path("tests/fixtures/vacancy-extract.json")
        bad_letter = (
            "Уважаемая команда! Работал в FakeCorp над Vue-проектами. "
            "Имею опыт TypeScript и JavaScript. Готов обсудить детали. "
        ) * 8

        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(
                json.dumps({"cover_letter_text": bad_letter}),
                encoding="utf-8",
            )
            plan = compose_application_plan(
                profile_path=profile_path,
                vacancy_path=vacancy_path,
                draft_path=draft_path,
            )
            errors = validate_application_plan(plan, profile_path)
            self.assertTrue(any("employers not in profile" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
